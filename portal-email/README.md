# Portal email templates (Supabase Auth)

Two branded templates for the physician portal at pci.healthfrontgroup.com. They replace Supabase's default
emails so the invitation and the password reset look like Health Front, not like Supabase.

| File | Supabase template | Subject to set |
|------|-------------------|----------------|
| `invite.html` | Authentication → Email Templates → **Invite user** (and **Confirm signup** if used) | `Su acceso al portal de credenciales de Health Front` |
| `recovery.html` | Authentication → Email Templates → **Reset password** | `Restablezca su contraseña del portal de credenciales` |

Both use only Supabase's own variables: `{{ .ConfirmationURL }}` and `{{ .Email }}`. The logo loads from
https://healthfrontgroup.com/assets/health-front-logo.png, which the public site already serves.

## Where to paste

1. Supabase → project → **Authentication → Email Templates**. Pick the template, replace the body with the file's
   full HTML, set the subject from the table, save. Use "Send test email" if the plan offers it.
2. **Authentication → URL Configuration**. Site URL `https://pci.healthfrontgroup.com`. Redirect URLs must include
   `https://pci.healthfrontgroup.com/**`. Without this the recovery link falls back to the login page.
3. **Authentication → SMTP Settings → Custom SMTP**. Sender email `credenciales@healthfrontgroup.com`, sender name
   `Health Front · Credenciales`. Without custom SMTP the email still leaves from Supabase's shared address, and
   Supabase's free sender is rate-limited and lands in spam more often. Any transactional provider works
   (Google Workspace SMTP relay, Resend, Postmark); the domain needs SPF and DKIM records at GoDaddy for it.

## What still shows Supabase

- **The link itself.** `{{ .ConfirmationURL }}` points at `<project>.supabase.co/auth/v1/verify?...`. The button
  hides it; the small fallback line at the bottom shows it. To make the link read `pci.healthfrontgroup.com`, either
  buy Supabase's custom auth domain add-on, or change the portal to accept `{{ .TokenHash }}` on its own page and
  call `verifyOtp` there. The second route also defeats Outlook Safe Links, which opens links to scan them and spends
  the one-time token before the physician clicks. That is portal code, not this repository.
- **The link preview** in iMessage or WhatsApp comes from the portal page's Open Graph tags (title, description,
  image). Also portal code.

## Sending by text instead of email

If the invitation goes by text message, copy the link from Supabase (Users → the user → Generate link) and send it
with a short note. One hour, one use, and ask them to open it from the phone, not from a corporate Outlook.
