/*
  Warnings:

  - Added the required column `birthday` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `password` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "User" ADD COLUMN     "birthday" TIMESTAMP(3) NOT NULL,
ADD COLUMN     "password" VARCHAR(128) NOT NULL;
