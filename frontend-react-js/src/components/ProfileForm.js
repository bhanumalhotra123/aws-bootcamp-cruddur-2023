// Importing CSS styles for the ProfileForm component
import './ProfileForm.css';

// Importing necessary modules and functions from React and other libraries
import React from "react";
import process from 'process';
import {getAccessToken} from 'lib/CheckAuth';

// Defining the ProfileForm component as a functional component
export default function ProfileForm(props) {
  // State variables to store bio and display name, initialized to 0
  const [bio, setBio] = React.useState(0);
  const [displayName, setDisplayName] = React.useState(0);

  // useEffect hook to update bio and display name when props.profile changes
  React.useEffect(()=>{
    console.log('useEffects',props)
    setBio(props.profile.bio);
    setDisplayName(props.profile.display_name);
  }, [props.profile])

  // Function to handle form submission
  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      // Constructing the backend URL
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`
      // Getting access token
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      // Sending POST request to update profile
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bio: bio,
          display_name: displayName
        }),
      });
      // Parsing response data
      let data = await res.json();
      // Handling success or failure of the request
      if (res.status === 200) {
        // Resetting bio and display name after successful update
        setBio(null)
        setDisplayName(null)
        // Closing the form
        props.setPopped(false)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  // Function to handle change in bio input field
  const bio_onchange = (event) => {
    setBio(event.target.value);
  }

  // Function to handle change in display name input field
  const display_name_onchange = (event) => {
    setDisplayName(event.target.value);
  }

  // Function to close the form when clicking outside
  const close = (event)=> {
    console.log('close',event.target)
    if (event.target.classList.contains("profile_popup")) {
      props.setPopped(false)
    }
  }

  // Rendering the form if props.popped is true
  if (props.popped === true) {
    return (
      <div className="popup_form_wrap profile_popup" onClick={close}>
        <form 
          className='profile_form popup_form'
          onSubmit={onsubmit}
        >
          <div class="popup_heading">
            <div class="popup_title">Edit Profile</div>
            <div className='submit'>
              <button type='submit'>Save</button>
            </div>
          </div>
          <div className="popup_content">
            <div className="field display_name">
              <label>Display Name</label>
              <input
                type="text"
                placeholder="Display Name"
                value={displayName}
                onChange={display_name_onchange} 
              />
            </div>
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
