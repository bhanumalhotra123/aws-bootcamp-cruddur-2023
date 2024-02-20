// Importing CSS styles from the external file './EditProfileButton.css'
import './EditProfileButton.css';

// Defining a functional component named EditProfileButton
export default function EditProfileButton(props) {
  // Define a function pop_profile_form that handles clicking on the button
  const pop_profile_form = (event) => {
    // Prevent the default behavior of the event (e.g., form submission)
    event.preventDefault();
    // Call the setPopped function passed as a prop with the argument true
    props.setPopped(true);
    // Return false to prevent any additional default behavior of the event
    return false;
  }

  // Render the component
  return (
    // Render a button element with an onClick event handler calling pop_profile_form function
    // Set the class name of the button to 'profile_edit_button'
    // Set the href attribute to '#' (This is not necessary for a button element)
    <button onClick={pop_profile_form} className='profile_edit_button' href="#">Edit Profile</button>
  );
}


//In simple terms, this code creates a button labeled "Edit Profile" that, when clicked, tells its parent component to show a profile editing form. The appearance of the button is styled using CSS from an external file.