-- Delete original data if any
drop database `lemon`;

-- Create database and tables
create database if not exists `lemon`;
use `lemon`;

create table if not exists `user`
(
    `username` varchar(40) primary key,
    `email`    varchar(40) unique,
    `password` char(40) not null
) engine = InnoDB
  default charset = utf8;

create table if not exists `survey`
(
    `index`        int primary key auto_increment,
    `title`        varchar(50)  not null,
    `username`     varchar(40)  not null,
    `desc`         varchar(200) null,
    `status`       bool         not null,
    `answer_type`  int          not null,
    `update_time`  varchar(20)  not null,
    `publish_time` varchar(20)  null,
    foreign key (`username`) references `user` (`username`)
) engine = InnoDB
  default charset = utf8
  auto_increment = 1;

create table if not exists `question`
(
    `index`          int primary key auto_increment,
    `title`          varchar(100) not null,
    `type`           int          not null,
    `survey_id`      int          not null,
    `question_index` int          not null,
    `num_choices`    int          not null,
    `num_min_chosen` int          not null,
    `num_max_chosen` int          not null,
    `single_row`     bool         null,
    `fill_digit`     bool         null,
    `levels`         int          null,
    `compulsory`     bool         not null,
    foreign key (`survey_id`) references `survey` (`index`) on delete cascade
) engine = InnoDB
  default charset = utf8
  auto_increment = 1;

create table if not exists `option`
(
    `index`        int primary key auto_increment,
    `question_id`  int          not null,
    `option_index` int          not null,
    `text`         varchar(100) not null,
    foreign key (`question_id`) references `question` (`index`) on delete cascade
) engine = InnoDB
  default charset = utf8
  auto_increment = 1;

create table if not exists `submit`
(
    `index`       int auto_increment primary key,
    `survey_id`   int         not null,
    `submit_ip`   varchar(20) not null,
    `username`    varchar(40) null,
    `submit_date` varchar(10) not null,
    foreign key (`survey_id`) references `survey` (`index`) on delete cascade,
    foreign key (`username`) references `user` (`username`)
) engine = InnoDB
  default charset = utf8
  auto_increment = 1;

create table if not exists `answer`
(
    `index`       int auto_increment primary key,
    `question_id` int          not null,
    `submit_id`   int          not null,
    `survey_id`   int          not null,
    `type`        int          not null,
    `content`     varchar(200) not null,
    foreign key (`question_id`) references `question` (`index`) on delete cascade,
    foreign key (`submit_id`) references `submit` (`index`) on delete cascade,
    foreign key (`survey_id`) references `survey` (`index`) on delete cascade
) engine = InnoDB
  default charset = utf8
  auto_increment = 1;
