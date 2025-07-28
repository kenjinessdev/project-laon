/*
  Warnings:

  - You are about to drop the column `customer_order_code` on the `customer_orders` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "customer_orders_customer_order_code_key";

-- AlterTable
ALTER TABLE "customer_orders" DROP COLUMN "customer_order_code";
