Reflection – Module 13: JWT, Frontend Integration, and CI/CD

Module 13 helped me understand how authentication, frontend interaction, and automated deployment workflows come together to create a complete full-stack system. The biggest shift was learning how JWT tokens work. Instead of maintaining sessions, the server generates a signed token that the frontend stores and sends with each request. This made me understand why JWT is stateless, scalable, and widely used in modern APIs.

Integrating the frontend forms with the FastAPI backend using JavaScript fetch() also gave me hands-on experience with real request–response flows. I learned how to send form data, handle errors, and display messages to users directly from JavaScript.

Setting up PostgreSQL in GitHub Actions was challenging at first because my tests failed with connection errors. Through debugging, I learned how services work in GitHub pipelines, how environment variables must match exactly, and why integration tests require a real running database. After fixing the connection string and ensuring tables were created during test setup, the CI pipeline became stable.

Playwright end-to-end tests were another important part of this module. Writing automated browser tests taught me how to simulate real user actions and verify the frontend.

Overall, this module significantly improved my practical understanding of secure authentication, frontend-backend communication, and automated testing pipelines.