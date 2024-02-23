"use strict";

// Importing the CognitoJwtVerifier class from the aws-jwt-verify package
const { CognitoJwtVerifier } = require("aws-jwt-verify");

// Initializing a jwtVerifier object with configuration parameters
const jwtVerifier = CognitoJwtVerifier.create({
  // The user pool ID obtained from environment variables
  userPoolId: process.env.USER_POOL_ID,
  // Specifying the token use as "id" indicating it represents user identity
  tokenUse: "access",
  // The client ID obtained from environment variables
  clientId: process.env.CLIENT_ID,
  // Custom JWT check (currently commented out)
  // customJwtCheck: ({ payload }) => {
  //   assertStringEquals("e-mail", payload["email"], process.env.USER_EMAIL);
  // },
});

// AWS Lambda function handler
exports.handler = async (event) => {
  // Logging the incoming request
  console.log("request:", JSON.stringify(event, undefined, 2));

  // Extracting the JWT token from the Authorization header of the request
  const jwt = event.headers.authorization;

  try {
    // Verifying the JWT token using jwtVerifier
    const payload = await jwtVerifier.verify(jwt);
    // If verification succeeds, logging the payload of the JWT token
    console.log("Access allowed. JWT payload:", payload);
  } catch (err) {
    // If verification fails, logging the error
    console.error("Access forbidden:", err);
    // Returning an object indicating authorization is forbidden
    return {
      isAuthorized: false,
    };
  }

  // If verification succeeds, returning an object indicating authorization is allowed
  return {
    isAuthorized: true,
  };
};
