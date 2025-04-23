document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorContainer = document.getElementById('login-error');

  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();

          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;

          try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ email, password })
          });

          // Vérifier la réponse de l'API dans la console
          const data = await response.json();
          console.log(data);  // Cela nous montrera la réponse complète

          if (response.ok) {
            console.log('Réponse OK:', data); // Log du data retourné par l'API
            document.cookie = `token=${data.access_token}; path=/`;
            console.log('Token enregistré, redirection...');
            window.location.href = 'index.html';
        } else {
            console.log('Erreur:', data.error);
            if (errorContainer) {
                errorContainer.textContent = data.error || 'Une erreur est survenue.';
                errorContainer.style.display = 'block';
            } else {
                alert(data.error || 'Erreur lors de la connexion');
            }
        }
      }catch (err) {
              if (errorContainer) {
                  errorContainer.textContent = 'Erreur de connexion au serveur.';
                  errorContainer.style.display = 'block';
              } else {
                  alert('Erreur réseau : ' + err.message);
              }
          }
      });
      function getCookie(name){
        const value = `;${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
  }
}
});
