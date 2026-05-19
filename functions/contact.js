export async function onRequestPost(context) {
  const { request, env } = context;

  const data    = await request.formData();
  const name    = (data.get('name')    || '').trim() || 'Anonim';
  const email   = (data.get('email')   || '').trim();
  const message = (data.get('message') || '').trim();

  if (!email || !message) {
    return Response.json({ ok: false, error: 'Brakuje emaila lub wiadomości.' }, { status: 400 });
  }

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'Cichy Mechanik <onboarding@resend.dev>',
      to: ['photocoffeeman@gmail.com'],
      reply_to: email,
      subject: `Wiadomosc od ${name} — cichymechanik.pl`,
      text: `Imie: ${name}\nEmail: ${email}\n\nWiadomosc:\n${message}`,
    }),
  });

  if (res.ok) {
    return Response.json({ ok: true });
  }

  const err = await res.json().catch(() => ({}));
  return Response.json({ ok: false, error: err.message || 'Blad wysylki.' }, { status: 500 });
}
