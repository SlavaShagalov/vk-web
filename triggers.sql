CREATE OR REPLACE FUNCTION on_question_score() RETURNS TRIGGER AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE app_question
        SET rating = rating + new.value
        WHERE id = new.question_id;
    ELSEIF TG_OP = 'DELETE' THEN
        UPDATE app_question
        SET rating = rating - old.value
        WHERE id = old.question_id;
    END IF;

    RETURN NULL;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER question_score
    AFTER INSERT OR DELETE
    ON app_questionscore
    FOR EACH ROW
EXECUTE PROCEDURE on_question_score();

CREATE OR REPLACE FUNCTION on_answer_score() RETURNS TRIGGER AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE app_answer
        SET rating = rating + new.value
        WHERE id = new.answer_id;
    ELSEIF TG_OP = 'DELETE' THEN
        UPDATE app_answer
        SET rating = rating - old.value
        WHERE id = old.answer_id;
    END IF;

    RETURN NULL;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER answer_score
    AFTER INSERT OR DELETE
    ON app_answerscore
    FOR EACH ROW
EXECUTE PROCEDURE on_answer_score();
