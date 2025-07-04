-- CreateEnum
CREATE TYPE "Role" AS ENUM ('farmer', 'customer');

-- CreateTable
CREATE TABLE "User" (
    "id" UUID NOT NULL,
    "first_name" VARCHAR(100) NOT NULL,
    "middle_name" VARCHAR(100) NOT NULL,
    "last_name" VARCHAR(100) NOT NULL,
    "suffix" VARCHAR(100) NOT NULL,
    "profile_image_url" TEXT,
    "email" VARCHAR(100) NOT NULL,
    "role" "Role" NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");
