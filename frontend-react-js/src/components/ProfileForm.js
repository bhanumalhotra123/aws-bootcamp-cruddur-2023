// Import CSS file and necessary dependencies
import './ProfileForm.css';
import React from "react"; // Import React library
import process from 'process'; // Import the 'process' module (Node.js built-in)
import {getAccessToken} from 'lib/CheckAuth'; // Import the 'getAccessToken' function from the 'CheckAuth' module

// Define a functional component named ProfileForm, which takes props as input
export default function ProfileForm(props) {
  // Initialize state variables 'bio' and 'displayName' using useState hook
  const [bio, setBio] = React.useState(''); // Initialize 'bio' state variable with an empty string
  const [displayName, setDisplayName] = React.useState(''); // Initialize 'displayName' state variable with an empty string

  // useEffect hook to update 'bio' and 'displayName' when props.profile changes
  React.useEffect(() => {
    // Update 'bio' state with props.profile.bio or an empty string if undefined
    setBio(props.profile.bio || '');

    // Update 'displayName' state with props.profile.display_name
    setDisplayName(props.profile.display_name);
  }, [props.profile]); // Run the effect whenever 'props.profile' changes

  // Function to fetch a presigned URL for uploading files to S3
  const s3uploadkey = async (extension)=> {
    // Log the file extension to the console
    console.log('ext',extension)
    try {
      // Get the API gateway URL from environment variables
      const gateway_url = process.env.REACT_APP_API_GATEWAY_ENDPOINT_URL;
      // Fetch the access token using the 'getAccessToken' function
      await getAccessToken();
      // Retrieve the access token from local storage
      const access_token = localStorage.getItem("access_token");
      // Create a JSON object with the file extension
      const json = {
        extension: extension
      };
      // Send a POST request to the API gateway to get the presigned URL
      const res = await fetch(gateway_url, {
        method: "POST",
        body: JSON.stringify(json),
        headers: {
          'Origin': process.env.REACT_APP_FRONTEND_URL,
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      // Parse the response JSON data
      let data = await res.json();
      // If the response status is 200, return the presigned URL
      if (res.status === 200) {
        return data.url;
      } else {
        // Log the response if the status is not 200
        console.log(res);
      }
    } catch (err) {
      // Log any errors that occur during the fetch operation
      console.log(err);
    }
  }

  // Function to handle file upload to S3
  const s3upload = async (event)=> {
    // Log the event details to the console
    console.log('event',event)
    // Get the file object from the event target
    const file = event.target.files[0];
    // Extract file details such as name, size, and type
    const filename = file.name;
    const size = file.size;
    const type = file.type;
    // Create a preview image URL for the file
    const preview_image_url = URL.createObjectURL(file);
    // Log file details to the console
    console.log(filename, size, type);
    // Split the filename to extract the file extension
    const fileparts = filename.split('.');
    const extension = fileparts[fileparts.length-1];
    // Get the presigned URL for uploading the file to S3
    const presignedurl = await s3uploadkey(extension);
    try {
      // Send a PUT request to upload the file to S3 using the presigned URL
      const res = await fetch(presignedurl, {
        method: "PUT",
        body: file,
        headers: {
          'Content-Type': type
      }});
      // Log the response if the status is not 200
      if (res.status !== 200) {
        console.log(res);
      }
    } catch (err) {
      // Log any errors that occur during the fetch operation
      console.log(err);
    }
  }

  // Function to handle form submission
  const onsubmit = async (event) => {
    // Prevent the default form submission behavior
    event.preventDefault();
    try {
      // Construct the backend URL for updating the user profile
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`;
      // Fetch the access token using the 'getAccessToken' function
      await getAccessToken();
      // Retrieve the access token from local storage
      const access_token = localStorage.getItem("access_token");
      // Send a POST request to update the user profile
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        // Send the user's bio and display name as JSON data in the request body
        body: JSON.stringify({
          bio: bio,
          display_name: displayName
        }),
      });
      // Parse the response JSON data
      let data = await res.json();
      // If the response status is 200, reset the form fields and close the popup
      if (res.status === 200) {
        setBio(null)
        setDisplayName(null)
        props.setPopped(false)
      } else {
        // Log the response if the status is not 200
        console.log(res)
      }
    } catch (err) {
      // Log any errors that occur during the fetch operation
      console.log(err);
    }
  }

  // Function to handle bio input field change
  const bio_onchange = (event) => {
    // Update the 'bio' state with the new value from the input field
    setBio(event.target.value);
  }

  // Function to handle display name input field change
  const display_name_onchange = (event) => {
    // Update the 'displayName' state with the new value from the input field
    setDisplayName(event.target.value);
  }

  // Function to close the popup when clicking outside the form
  const close = (event)=> {
    // Check if the clicked element has the 'profile_popup' class
    if (event.target.classList.contains("profile_popup")) {
      // Close the popup by setting 'props.popped' to false
      props.setPopped(false)
    }
  }

  // Render the profile form component
  if (props.popped === true) {
    return (
      <div className="popup_form_wrap profile_popup" onClick={close}>
        <form 
          className='profile_form popup_form'
          onSubmit={onsubmit}
        >
          <div className="popup_heading">
            <div className="popup_title">Edit Profile</div>
            <div className='submit'>
              <button type='submit'>Save</button>
            </div>
          </div>
          <div className="popup_content">
            {/* File input field for uploading avatar */}
            <input type="file" name="avatarupload" onChange={s3upload} />

            {/* Input field for editing display name */}
            <div className="field display_name">
              <label>Display Name</label>
              <input
                type="text"
                placeholder="Display Name"
                value={displayName}
                onChange={display_name_onchange} 
              />
            </div>

            {/* Textarea field for editing bio */}
            <div className="field bio">
              <label>Bio</label>
              <textarea
                placeholder="Bio"
                value={bio}
                onChange={bio_onchange} 
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}

