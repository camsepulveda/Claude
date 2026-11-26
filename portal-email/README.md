# Portal email templates (Supabase Auth)

Two branded templates for the physician portal at pci.healthfrontgroup.com. They replace Supabase's default
emails so the invitation and the password reset look like Health Front, not like Supabase.

| File | Supabase template | Subject to set |
|------|-------------------|----------------|
| `invite.html` | Authentication → Email Templates → **Invite user** (and **Confirm signup** if used) | `Su acceso al portal de credenciales de Health Front` |
| `recovery.html` | Authentication → Email Templates → **Reset password** | `Restablezca su contraseña del portal de credenciales` |

Both link to `{{ .RedirectTo }}?token_hash={{ .TokenHash }}&type=recovery`, the mechanism the portal already uses
(as of 2026-11-26): the link opens on pci.healthfrontgroup.com and the portal asks for a **Continuar** click before it
spends the token, so a mail scanner such as Outlook Safe Links cannot consume it. `{{ .Email }}` fills the footer.
Both templates are recovery-type on purpose: first access is sent as a password recovery, as the existing Supabase
template does. Generate links with the redirect set to `https://pci.healthfrontgroup.com/portal/`, or
`{{ .RedirectTo }}` falls back to the Site URL. The logo loads from
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

- **The sender address**, until custom SMTP is set (step 3 above).
- **The link preview** in iMessage or WhatsApp comes from the portal page's Open Graph tags (title, description,
  image). Also portal code.

## Sending by text instead of email

If the invitation goes by text message, copy the link from Supabase (Users → the user → Generate link) and send it
with a short note. One hour, one use, and ask them to open it from the phone, not from a corporate Outlook.
