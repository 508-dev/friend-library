# Spec

This is a project spec document for the Stuff for Friends Library project. It describes how this project should be implemented. LLMs should view this and implement the project per this document.

## Summary

This app is a library of your things, which your friends can view and borrow. A given user's friends have controlled readonly visibility (via secret link) to the user's stuff. They can see what's available, and optionally per the user's choice, who's currently borrowing an unavailable thing, as well as optionally, for how long. The friends can then request to borrow something.

The user can their stuff available to borrow, and see who's borrowing what, and for how long.

For example, if you have a collection of CDs you don't often listen to, you can list the CDs individually so that your friends can borrow a couple.

## UX Details

The front page of the app when not logged in is mildly marketing-esque, demonstrating the features of the app in brief, but this isn't the main marketing page so this shouldn't be too prominent. Mostly this page is designed to get the user to login or request registration against the given instance of the app.

Once logged in, a user will be faced with an overview page showing a shortlist of requested borrows, any ongoing lendings, and a general overview of how much stuff they have on offer to their friends. This view has quick access to add new stuff.

Prominently displayed is a URL like `lending.example.com/{{hash}}`, which is a given user's private lending page. For now, there's no other authentication to view a given user's lending page.

If friends view the private lending page link, they're taken to a gallery-like list view of things that given user is lending out. There's an input box at the top prominently displayed for them to enter their name. All "request borrow" buttons are disabled until the user's name is in that input box. Each gallery item has a "request borrow" button, as well as showing some basic information about the item. Optionally per the user's preferences, the gallery shows lent items and optionally, who is borrowing currently unavailable items.

Gallery items have a detail view, accessible by clicking a "more info..." button. This opens the gallery item in its own page such as `lending.example.com/{{hash}}/{{item_id}}`. This shows all available information about the object, as well as optionally per the given users' preferences, lending history for the object.

The logged in user also has a setting page where they can set the following settings:

1. Whether friends can see borrowed items on the lending list page.
2. (only enabled if 1 is toggled) Whether friends can see who has borrowed an item.
3. Whether friends can see lending history of an item in its detail page
4. (only enabled if 3 is toggled) Whether friends can see the name of previous borrowers in the lending history of an item on its detail page.

The main overview page "recent borrow requests" section is one place where borrows can be approved, but there's also an "all borrow requests" page. Both show borrow requests as a list of items, with the requested item name, the requested borrower's name, and "approve" or "deny" buttons. If a borrow has been approved, then it's in a "pending" state, with an option to mark it as "lent out," indicating that the borrowing has begun. At this point, it no longer appears in a "borrow request" section or page.

There's views of ongoing lendings: one shortlist on the main logged in landing page, and another in a "all current lendings" page. Both display as a list of borrowed items, who's borrowing, and a "mark as returned" button. Marking an item as returned makes it available for borrowing, thus it will no longer be displayed in an "ongoing lendings" view.

There's list views of unborrowed items, both on the landing page and in an "all items" view. Items can be marked as "unavailable to borrow" or toggled back to "available to borrow." Both are always visible in the "all items" view. There's also a prominent way to add new items. Items can be individually removed, with a confirmation dialog confirming.

Items for lending have the following properties:

1. Image (optional)
2. Title
3. Short description (shown on list page) (optional)
4. Long description (optional)
5. Borrow time limit (optional, assumed none by default, freeform text input)

Items acquire the following attributes, but they aren't set by the user:

1. Borrow history (who, when borrowed, when returned)

## UI Design and Styling

The design is warm and hobbit-like. Cottagecore friendvibes. Crumbly scones, butter, jam, tea. Polished and well-worn wood. Nooks and crannies filled with delightful bric-brac.

## Implementation Details

**Stack:** Django + HTMX app. CSS is styled without any libraries. Only modern browsers are targeted. PostgreSQL DB.

**Development:**

- Docker Compose dev file spins up PostgreSQL
- `django-browser-reload` for automatic browser refresh on file changes
- Standard `python manage.py runserver` for Django

**Production:**

- Docker Compose bundles PostgreSQL, and Django
- WhiteNoise serves static files directly from Django (no separate Nginx needed)
- Deployed on push to main via Coolify

**Testing:**

- Backend: `pytest` + `pytest-django` with `factory_boy` for model factories
- Frontend/E2E: Playwright for browser testing of HTMX interactions

**TypeScript:** Any JavaScript necessary is TypeScript.
