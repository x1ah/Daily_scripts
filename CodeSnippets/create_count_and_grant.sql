/* 在本机 MySQL 数据库创建一个用户名为 myname，密码为 password 的用户，
 * 并且把 test 这个数据库的所有权限授予给 myname 用户
 */
CREATE DATABASE test;
USE test;
CREATE USER 'myname'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON test.* TO 'myname'@'localhost';
