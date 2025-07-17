-- CreateEnum
CREATE TYPE "ProductStatus" AS ENUM ('draft', 'active', 'archived', 'sold');

-- CreateEnum
CREATE TYPE "ProductVisibility" AS ENUM ('public', 'private');

-- AlterTable
ALTER TABLE "products" ADD COLUMN     "status" "ProductStatus" NOT NULL DEFAULT 'active',
ADD COLUMN     "visibility" "ProductVisibility" NOT NULL DEFAULT 'public';
