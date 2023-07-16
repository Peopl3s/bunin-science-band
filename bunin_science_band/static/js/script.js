const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };
  

  function enableLikes() {

    const likeBtn = document.getElementById('like');
    const eventId = likeBtn.dataset.eventId;
    const resource = likeBtn.dataset.resource;
    let likeCounter = document.getElementById('like-count');

    likeBtn.addEventListener('click', event => {
      event.preventDefault()

      fetch(`/${resource}/${resource}_like/%7B${eventId}%7D`, {
         method: 'POST',
         headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
          },
         body: {}
      }).then(
         response => {
            return response.json();
         }
      ).then(
         data => {
          likeCounter.innerHTML =  data.likes_count;
         }
      ).catch(error => console.error(error));
  });
}

window.onload = enableLikes;