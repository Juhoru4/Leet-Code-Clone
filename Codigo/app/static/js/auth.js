const out = document.getElementById('output');
    function show(obj){ out.textContent = JSON.stringify(obj, null, 2); }

    async function post(path, body){
      const res = await fetch(path, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      try { return await res.json(); } catch(e){ return { status: res.status }; }
    }

    document.getElementById('register-form').addEventListener('submit', async e => {
      e.preventDefault();
      const f = e.target;
      const body = { email: f.email.value, password: f.password.value, username: f.username.value, full_name: f.full_name.value, role: f.role.value };
      const r = await post('/auth/register', body);
      show(r);
      if (r && r.redirect_url) {
        window.location.href = r.redirect_url;
      }
    });

    document.getElementById('login-form').addEventListener('submit', async e => {
      e.preventDefault();
      const f = e.target;
      const body = { email: f.email.value, password: f.password.value };
      const res = await fetch('/auth/login', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      if (res.redirected) {
        window.location.href = res.url;
      } else if (res.ok) {
        window.location.href = '/problems/ui';
}
    });

    document.getElementById('btn-logout').addEventListener('click', async () => {
      const res = await fetch('/auth/logout', { method: 'POST', credentials: 'include' });
      try{ show(await res.json()); } catch(e){ show({ status: res.status }); }
    });

    document.getElementById('btn-me').addEventListener('click', async () => {
      const res = await fetch('/auth/me', { method: 'GET', credentials: 'include' });
      try{ show(await res.json()); } catch(e){ show({ status: res.status }); }
    });