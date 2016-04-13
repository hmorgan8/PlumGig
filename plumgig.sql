-- DROP DATABASE IF EXISTS plumgig;
-- CREATE DATABASE plumgig;
-- \c plumgig
-- CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(
    username varchar(30) NOT NULL PRIMARY KEY,
    password varchar(80) NOT NULL,
    bio text
);

INSERT INTO users VALUES ('Hannah',crypt('h', gen_salt('bf')), 'this is Hannah''s bio');
INSERT INTO users VALUES ('Scott',crypt('s', gen_salt('bf')));
INSERT INTO users VALUES ('Morgan',crypt('m', gen_salt('bf')));

DROP TABLE IF EXISTS videos CASCADE;
CREATE TABLE videos(
    vid_id serial NOT NULL PRIMARY KEY,
    username varchar(30) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE,
    URL varchar(100) NOT NULL,
    title varchar(40) NOT NULL,
    technique varchar(20) NOT NULL,
    genre varchar(40) NOT NULL,
    
    CONSTRAINT users_username_fk
    FOREIGN KEY (username)
    REFERENCES users (username)
);

INSERT INTO videos (username, URL, title, technique, genre) VALUES ('Hannah','https://www.youtube.com/embed/jAjM7cO2znw','Lindt','objects','playful object'),('Hannah','https://www.youtube.com/embed/x_SjQtwskog','Sever','photography','narrative'),('Scott','https://www.youtube.com/embed/pXU4J_cOx1Y','Straight Into Your Arms','objects','music video'),('Scott','https://player.vimeo.com/video/97718226','Tharsis Sleeps','textile','music video'),('Scott','https://www.youtube.com/embed/fEPqgSNLfK8','The Little Prince','CGI/stop-motion','movie trailer'),('Morgan','https://www.youtube.com/embed/gpum4nK2wOM','Aug(DE)mented Reality','hand-drawn','funny'),('Morgan','https://player.vimeo.com/video/159620115','DST','2D CGI','playful object');
                                                                                                                                                                                                                                                                                                                                                                        --"https://player.vimeo.com/video/97718226"                                                                                                                                                               https://www.youtube.com/watch?v=gpum4nK2wOM

DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews(
    review_id SERIAL NOT NULL PRIMARY KEY,
    reviewer varchar(30) NOT NULL,
    vid_id INT NOT NULL,
    total_score INT NOT NULL,
    quality_score INT NOT NULL,
    originality_score INT NOT NULL,
    impact_score INT NOT NULL,
    quality_text text,
    originality_text text,
    impact_text text,
    
    CONSTRAINT users_username_fk
    FOREIGN KEY (reviewer)
    REFERENCES users (username),
    
    CONSTRAINT videos_vidid_fk
    FOREIGN KEY (vid_id)
    REFERENCES videos (vid_id)
);

INSERT INTO reviews (reviewer,vid_id,total_score,quality_score,originality_score,impact_score,quality_text,originality_text,impact_text) VALUES ('Hannah','6','7','8','6','7','quality was good','originality was fine','impactful');

GRANT ALL ON users TO aziz;
GRANT ALL ON videos TO aziz;
GRANT ALL ON reviews TO aziz;
GRANT ALL ON videos_vid_id_seq TO aziz;
GRANT ALL ON reviews_review_id_seq TO aziz;