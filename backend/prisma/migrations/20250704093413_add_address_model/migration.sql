/*
  Warnings:

  - Added the required column `phone_number` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "User" ADD COLUMN     "phone_number" VARCHAR(50) NOT NULL;

-- CreateTable
CREATE TABLE "addresses" (
    "address_id" SERIAL NOT NULL,
    "user_id" UUID NOT NULL,
    "street" TEXT NOT NULL,
    "street2" TEXT,
    "city" VARCHAR(50) NOT NULL,
    "region" VARCHAR(50) NOT NULL,
    "postal_code" VARCHAR(20) NOT NULL,
    "is_primary" BOOLEAN NOT NULL,

    CONSTRAINT "addresses_pkey" PRIMARY KEY ("address_id")
);

-- AddForeignKey
ALTER TABLE "addresses" ADD CONSTRAINT "addresses_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
