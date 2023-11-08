from fastapi import APIRouter, Depends, Header, Request, HTTPException
from dotenv import dotenv_values 
from fastapi.responses import RedirectResponse
import stripe, json
from database.firebase import db
from routers.router_auth import auth, get_current_user

env = dotenv_values('.env')
stripe_config=json.loads(env['STRIPE_CONFIG'])

router = APIRouter(
    prefix='/stripe',
    tags=['Stripe']
)

stripe.api_key=stripe_config['secret_key']

@router.get('/subscribe')
async def get_checkout(user_data: dict = Depends(get_current_user)):
    query_result=db.child('users').child(user_data['uid']).child('stripe').get().val()
    if query_result : raise HTTPException(status_code=400, detail='user already subscribed')
    
    checkout_session = stripe.checkout.Session.create(
        success_url = env['YOUR_DOMAIN']+'/success.html',
        cancel_url = env['YOUR_DOMAIN']+'/cancel.html',
        line_items=[
            {
                "price": stripe_config['price_id'],
                "quantity": 1,
            }
        ],
        mode="subscription",
        payment_method_types = ['card'],
        customer_email=user_data['email']
    )
    return checkout_session['url']
    return RedirectResponse(checkout_session['url'])

@router.get('/unsubscribe')
async def unsubscribe_user(user_data: dict = Depends(get_current_user)):
    query_result=db.child('users').child(user_data['uid']).child('stripe').get().val()
    if not query_result : raise HTTPException(status_code=400, detail='user not subscribed')
    
    db.child('users').child(user_data['uid']).child('stripe').remove()
    stripe.Subscription.delete(query_result['subscription_id'])


@router.post('/webhook')
async def retreive_webhook(request: Request, STRIPE_SIGNATURE: str=Header()):
    event = None
    payload = await request.body()
    sig_header = STRIPE_SIGNATURE
    
    #constructing webhook event
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_config['webhook_secret']
        )
    except ValueError as e:
        print('Invalid payload in POST /stripe/webhook response-body')
        raise e
    except stripe.error.SignatureVerificationError as e:
        print('Invalid signature in POST /stripe/webhook response-header')
        raise e
    #event handler
    if event['type'] == 'checkout.session.completed': print('Checkout session completed')
    elif event['type'] == 'invoice.paid':
        print('Invoice paid')
        email = event['data']['object']['customer_email']
        firebase_user = auth.get_user_by_email(email)
        customer_id = event['data']['object']['customer']
        subscription_id = event['data']['object']['subscription']
        db.child('users').child(firebase_user.uid).child('stripe').set(
            data={
                'subscription_id':subscription_id,
                'customer_id':customer_id
            }
        )
    elif event['type'] == 'invoice.payment_failed': print('Invoice payment failed')
    else: print('Unhandled event type {}'.format(event['type']))

@router.get('/usage')
async def stripe_usage(userData: int = Depends(get_current_user)):
    fireBase_user= auth.get_user(userData['uid'])
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    cust_id = stripe_data["cust_id"]
    return stripe.Invoice.upcoming(customer=cust_id)
