export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const data = await request.formData();
    const name    = (data.get('name')    || '').trim() || 'Anonim';
    const email   = (data.get('email')   || '').trim();
    const message = (data.get('message') || '').trim();

    if (!email || !message) {
      return Response.json({ ok: false, error: 'Brakuje emaila lub wiadomości.' }, { status: 400 });
    }

    const body = [
      `Wiadomość z formularza cichymechanik.pl`,
      ``,
      `Imię:    ${name}`,
      `Email:   ${email}`,
      ``,
      `Wiadomość:`,
      message,
    ].join('\n');

    const raw = [
      'From: kontakt@cichymechanik.pl',
      'To: photocoffeeman@gmail.com',
      `Subject: =?utf-8?B?${btoa(unescape(encodeURIComponent(`Wiadomość od ${name} — cichymechanik.pl`)))}?=`,
      'Content-Type: text/plain; charset=utf-8',
      '',
      body,
    ].join('\r\n');

    const msg = new EmailMessage('kontakt@cichymechanik.pl', 'photocoffeeman@gmail.com', raw);
    await env.SEND_EMAIL.send(msg);

    return Response.json({ ok: true });
  } catch (e) {
    return Response.json({ ok: false, error: e.message }, { status: 500 });
  }
}
