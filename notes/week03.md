# Week03

## Decentralized Authentication


- Decentralized Authentication: AWS Cognito facilitates authentication for our application.

- User Pool Management: Cognito serves as a centralized repository for user pools, enabling efficient management of user profiles.

JSON Web Tokens (JWTs): Upon successful authentication, Cognito issues JWTs, digitally signed and containing user claims, to authenticate users.

Token Verification: Our application verifies JWT signatures using Cognito's public key, ensuring their authenticity.

Authorization: Extracting user information from JWT claims, such as username or user ID, our application authorizes and grants access to requested resources.

Token Handling: Cognito's user pool identity SDKs for various platforms streamline token management, enhancing authentication processes.




![Cognito-UserPool1](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/b06cda0d-79fb-4b30-ad9f-d28418eb2e20)

Setup: Setting up a Cognito User pool involves initiating the process via the AWS console, navigating to Cognito, and selecting "Create a user pool" to configure the user directory for seamless user management within our application.

![Cognito-UserPool2](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/93863d24-79bf-4c15-9064-7ad88bb6876b)

  
![App Client](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/0f8e2f79-d42e-4e5b-9c2b-ac5fae690ade)

> In AWS Cognito, an "app client" represents a configuration entity that allows your application to interact securely with the Cognito user pool.


With our user pool setup, we needed to pass the variables we set here into our docker-compose.yml under frontend file:

```
      REACT_APP_AWS_PROJECT_REGION: "${AWS_DEFAULT_REGION}"
      REACT_APP_AWS_COGNITO_REGION: "${AWS_DEFAULT_REGION}"
      REACT_APP_AWS_USER_POOLS_ID: "us-east-1_XXXXXXXXXX"
      REACT_APP_CLIENT_ID: "xxxxxxxxxxxxxxxxxxxxx"
```
  
Install AWS Amplify
```
npm i aws-amplify --save
```

  
To allow the application to interact with our AWS Cognito User Pool,  AWS Amplify is used. 
  
Add it to our ‘App.js’ file and store our environment variables as we did above. We hook our Cognito User Pool into our app, by adding code to ‘App.js’


```
import { Amplify } from 'aws-amplify';
  
Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
```
> This JavaScript code initializes AWS Amplify, a JavaScript library provided by AWS for building scalable and secure cloud-powered applications, particularly for authentication using AWS Cognito, which is Amazon's managed user directory service.

  
- AWS Amplify: A JavaScript library provided by AWS to build scalable and secure cloud-powered applications.
- AWS Cognito: Amazon's managed user directory service, enabling user authentication and management in the cloud.
- Auth Section: A subsection within the configuration object used to specify authentication-related settings, such as Cognito user pool details.
- OAuth 2.0: An open standard for authorization that allows secure authorization of users' access to resources in a web application.
- JWT Usage: The React application receives the JWT and can use it to securely access protected resources or make authenticated requests to backend APIs. The application typically includes the JWT in the authorization header of HTTP requests when accessing protected endpoints.
- __Information Flow__: During runtime, the React application retrieves environment variables containing AWS region, Cognito user pool ID, and client ID. Amplify then utilizes this information to interact with Cognito for user authentication. When a user attempts to log in, the React application sends authentication requests to Cognito, which verifies the user's credentials. Upon successful authentication, Cognito issues JSON Web Tokens (JWTs) to the application, allowing the user access to protected resources.
  
  
  
HomeFeedPage.js
  
![Changes in HomePage](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/a6cc2d5a-aeac-4617-a35f-bb8789ccb70b)
  
This code is a React component called HomeFeedPage that renders a home feed page with various components like navigation, sidebar, and activity feed.
It imports necessary CSS and libraries like aws-amplify for authentication.
The checkAuth function checks if a user is authenticated using AWS Cognito, fetching user data if authenticated and setting it in the component's state.
The useEffect hook is used to trigger the authentication check when the component mounts, ensuring it runs only once.
The dataFetchedRef.current check prevents redundant authentication checks, ensuring it only happens once.
Overall, this component sets up authentication using AWS Cognito and renders a home feed page with relevant components.




Profile.js

![Changes in Profile.js](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/fdfa2f73-61b1-4448-8a15-b55b5703852b)
  
>This React component, ProfileInfo, is responsible for displaying user profile information and handling authentication using AWS Amplify. Let's break it down:
>State Management: The component uses React's useState hook to manage the popped state, which determines whether additional profile information is displayed (true) or not (false).
>Click Handler: The click_pop function toggles the popped state when the profile information is clicked. This allows users to expand or collapse the additional information.
>Sign Out Function: The signOut function is an asynchronous function that signs the user out using AWS Amplify's Auth.signOut() method. Upon successful sign-out, it redirects the user to the home page (/). Any errors encountered during the sign-out process are logged to the console.





