# [anime-list-api](https://anime-list-api-ibbi.onrender.com/)

## Anime List API

The **Anime router** regroups all animes that can be added to watchlists.<br>
Using the _/anime_ route you can :

- Get all animes.
- Add a new anime.
- Get an anime by id.
- Search an anime by name and category.
- Update an anime.
- Delete an anime.

The **Watchlist router** regroups users watchlist.<br>
Using the _/watchlist_ route you can :

- Get all watchlists.
- Add a new anime to the watchlist.
- Update a watchlist.

The **Stripe router** is used to pay a subscription and access the watchlist route.<br>
Using the _/stripe you can :
- Subscribe to the API
- Unsubscribe from the API

The **Auth router** is used to register user, registered users can subscribe to the API.<br>
Using the _/auth_ route you can :
- Sign up
- Login
- Get informations about your account