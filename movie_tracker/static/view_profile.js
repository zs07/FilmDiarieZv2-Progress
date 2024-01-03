// Handle form submission for follow/unfollow
document.addEventListener('DOMContentLoaded', () => {
    const followForm = document.getElementById('follow-form');
  
    if (followForm) {
      followForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const response = await fetch(followForm.action, {
          method: followForm.method,
          headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
        });
  
        try {
          const data = await response.json();
  
          if (response.ok) {
            const followButton = document.querySelector('.follow-button');
            followButton.innerText = data.following ? 'Unfollow' : 'Follow';
            followButton.classList.toggle('following', data.following);
          } else {
            console.error('Error:', data.message);
          }
        } catch (error) {
          console.error('JSON Parsing Error:', error);
          window.location.reload();
        }
      });
    }
  });
  