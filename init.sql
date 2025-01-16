DELETE FROM todostates;
-- Todostate ids also define the order of todo evolution. All todos start from state 1 and are
-- incremented by 1 until they are in the final state.
INSERT INTO todostates (id, state)
VALUES (1, 'Todo');
INSERT INTO todostates (id, state)
VALUES (2, 'In progress');
INSERT INTO todostates (id, state)
VALUES (3, 'Done');