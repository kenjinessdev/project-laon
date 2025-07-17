/*
  Warnings:

  - Added the required column `barangay` to the `addresses` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "addresses" ADD COLUMN     "barangay" TEXT NOT NULL;
