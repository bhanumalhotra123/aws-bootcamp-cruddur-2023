-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('bhanumalhotra','cloudevops101@gmail.com', 'bhanumalhotra' ,'MOCK'),
  ('bhanu', 'bhanumanaws@gmail.com', 'bhanuman','MOCK'),
  ('Bhanu Malhotra','bhanumalhotra219@gmail.com', 'Bhanu', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'bhanumalhotra' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )