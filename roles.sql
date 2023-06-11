CREATE ROLE qa_guest;
CREATE ROLE qa_member;
CREATE ROLE qa_admin;

ALTER ROLE qa_guest PASSWORD 'qa_guest_pswd';
ALTER ROLE qa_member PASSWORD 'qa_member_pswd';
ALTER ROLE qa_admin PASSWORD 'qa_admin_pswd';

ALTER ROLE qa_guest LOGIN;
ALTER ROLE qa_member LOGIN;
ALTER ROLE qa_admin LOGIN;

-- Назначение разрешений для роли qa_guest
GRANT SELECT ON app_profile TO qa_guest;
GRANT SELECT ON app_answer TO qa_guest;
GRANT SELECT ON app_question TO qa_guest;
GRANT SELECT ON app_answerscore TO qa_guest;
GRANT SELECT ON app_questionscore TO qa_guest;
GRANT SELECT ON app_label TO qa_guest;
GRANT SELECT ON app_question_labels TO qa_guest;
GRANT SELECT ON auth_user TO qa_guest;

-- Назначение разрешений для роли qa_member
GRANT SELECT, INSERT, UPDATE, DELETE ON app_profile TO qa_member;
GRANT SELECT, INSERT, UPDATE, DELETE ON app_answer TO qa_member;
GRANT SELECT, INSERT, UPDATE, DELETE ON app_question TO qa_member;
GRANT SELECT, INSERT, UPDATE, DELETE ON app_answerscore TO qa_member;
GRANT SELECT, INSERT, UPDATE, DELETE ON app_questionscore TO qa_member;
GRANT SELECT, INSERT, UPDATE, DELETE ON app_label TO qa_member;
GRANT SELECT, INSERT, UPDATE, DELETE ON app_question_labels TO qa_member;

-- Назначение разрешений для роли qa_admin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO qa_admin;

-- SELECT * FROM app_answer;