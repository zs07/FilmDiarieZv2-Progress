// Toggle the visibility of the edit profile form
function toggleEditProfile() {
    var formDiv = document.getElementById("edit-profile-form");
    formDiv.style.display = formDiv.style.display === "none" ? "block" : "none";
  }
  
  // Save profile changes asynchronously
  async function saveChanges() {
    var bio = document.getElementById("edit-bio").value;
    var socialMedia = document.getElementById("edit-social-media").value;
    var profilePictureInput = document.getElementById("edit-profile-picture");
    var profilePicture = profilePictureInput.files[0];
  
    var formData = new FormData();
    formData.append('bio', bio);
    formData.append('social_media', socialMedia);
    formData.append('profile_picture', profilePicture);
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
  
    try {
      const response = await fetch('/update_profile/', {
        method: 'POST',
        body: formData
      });
  
      const data = await response.json();
  
      if (data.bio !== undefined) {
        document.getElementById("bio").innerText = data.bio;
      }
  
      if (data.social_media !== undefined) {
        document.getElementById("social-media-container").innerHTML = `<ul class="social-media-links"><li><a href="${data.social_media}">${data.social_media}</a></li></ul>`;
      }
  
      if (data.profile_picture_url !== undefined) {
        document.querySelector(".profile-picture").src = data.profile_picture_url;
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  