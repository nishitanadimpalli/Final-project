Final Project Reflection

For this final project, I extended my FastAPI calculator application by adding a new feature: User Calculation Statistics. This feature allows authenticated users to view summaries of all calculations they have performed, including total count, per-type counts, and the average values for operands A and B. This enhancement required backend logic, a new route, database querying, and a new front-end statistics page.

What I Built

Implemented a new /calculations/stats API route in FastAPI.

Created a summarize_calculations() function to compute totals, averages, and counts.

Added a new front-end page (stats.html) with a button that loads stats dynamically using JavaScript.

Ensured authentication by requiring a valid JWT token for stats access.

Updated test suite with:

Unit tests for stats logic

Integration tests to verify authenticated stats route

End-to-end Playwright test for full workflow (register → login → calculate → view stats)

What I Learned

This project helped reinforce several important concepts:

Full-stack development workflow: connecting backend routes, business logic, templates, and JS fetch requests.

JWT authentication: securing pages and APIs using tokens stored in localStorage.

Database interaction with SQLAlchemy: filtering by user and aggregating results.

Playwright E2E testing: simulating real user interactions to ensure the UI + backend behave correctly.

CI/CD pipelines: running tests automatically, building Docker images, and deploying them to Docker Hub.

Debugging complex systems: especially resolving asynchronous issues between the UI, tests, and backend.

Challenges I Faced

The largest challenge was getting the Playwright E2E test to pass. Issues such as missing element IDs, timing delays, and unauthorized access required careful debugging. Another challenge was ensuring integration tests used the test database instead of the production one. Fixing these strengthened my understanding of automated testing and environment configuration.

Final Result

In the end, all tests passed, the feature works smoothly in the browser, and the automated pipeline successfully pushes images to Docker Hub. This project improved my ability to build real, testable, deployable applications — skills directly useful in professional software development.