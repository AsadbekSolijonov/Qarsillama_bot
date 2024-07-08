import logging
import os
import sqlite3
from abc import ABC, abstractmethod

from loader import BASE_DIR

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class Model(ABC):
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(CURRENT_DIR, 'sqlite3.db'))
        self.curr = self.conn.cursor()
        self.create_table()

    @abstractmethod
    def create_table(self):
        pass


class UserDB(Model):
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY NOT NULL,
                    username TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL);"""
        try:
            with self.conn:
                self.curr.execute(query)
                logging.info("Successfully created `users` table")
        except Exception as e:
            logging.error(f"Error creating table: {e}")

    def save(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO users ({columns}) VALUES ({placeholders});"
        try:
            with self.conn:
                self.curr.execute(query, values)
                logging.info(f"Successfully saved `users` table: {kwargs}")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def get(self, chat_id, *args):
        columns = ', '.join(args) if args else '*'
        query = f"SELECT {columns} FROM users WHERE id = ?;"
        try:
            with self.conn:
                self.curr.execute(query, (chat_id,))
                result = self.curr.fetchall()
                logging.info(f"Successfully retrieved data from `users` table for id {chat_id}")
                return result
        except Exception as e:
            logging.error(f"Error retrieving data: {e}")
            return None

    def delete(self, chat_id):
        query = f"DELETE FROM users WHERE id = ?;"
        try:
            with self.conn:
                self.curr.execute(query, (chat_id,))
                logging.info(f"Successfully deleted user with id {chat_id}")
        except Exception as e:
            logging.error(f"Error deleting data: {e}")


import logging


class ProductDB(Model):
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS product (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    picture BLOB NOT NULL);"""
        try:
            with self.conn:
                self.curr.execute(query)
                logging.info("Successfully created `product` table")
        except Exception as e:
            logging.error(f"Error creating table: {e}")

    def save(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO product ({columns}) VALUES ({placeholders});"
        try:
            with self.conn:
                self.curr.execute(query, values)
                logging.info(f"Successfully saved `product` table: {kwargs}")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def bimg(self, img_path):
        try:
            with open(img_path, 'rb') as f:
                new_image = f.read()
                logging.info(f"Successfully read image from {img_path}")
                return new_image
        except Exception as e:
            logging.error(f"Error reading image from {img_path}: {e}")
            return None

    def revert_image(self, binary_data, output_path):
        try:
            with open(output_path, 'wb') as file:
                file.write(binary_data)
                logging.info(f"Successfully wrote image to {output_path}")
                return output_path
        except Exception as e:
            logging.error(f"Error writing image to {output_path}: {e}")
            return None

    def get(self, **kwargs):
        query = "SELECT * FROM product;"
        if kwargs:
            query = f"SELECT * FROM product WHERE id={kwargs.get('id')};"
        try:
            with self.conn:
                self.curr.execute(query)
                result = self.curr.fetchall()
                logging.info(f"Successfully retrieved all data from `product` table")
                return result
        except Exception as e:
            logging.error(f"Error retrieving data: {e}")
            return None

    def delete(self, pk):
        query = "DELETE FROM product WHERE id = ?;"
        try:
            with self.conn:
                self.curr.execute(query, (pk,))
                logging.info(f"Successfully deleted product with id {pk}")
        except Exception as e:
            logging.error(f"Error deleting data: {e}")


class OrderDB(Model):
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    transaction_id INTEGER,
                    paid BOOLEAN NOT NULL DEFAULT FALSE,
                    delivered BOOLEAN NOT NULL DEFAULT FALSE,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(product_id) REFERENCES product(id));"""
        try:
            with self.conn:
                self.curr.execute(query)
                logging.info("Successfully created `orders` table")
        except Exception as e:
            logging.error(f"Error creating table: {e}")

    def save(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO orders ({columns}) VALUES ({placeholders});"
        try:
            with self.conn:
                self.curr.execute(query, values)
                logging.info(f"Successfully saved `orders` table: {kwargs}")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def get(self, user_id, product_id):
        query = f"""SELECT id FROM orders WHERE user_id={user_id} AND product_id={product_id};"""
        order_id = self.curr.execute(query).fetchone()
        return order_id

    def get_basket(self, user_id, paid=False):
        query = f"""SELECT
                    orders.user_id,
                    order_item.order_id,
                    orders.product_id,
                    order_item.count,
                    orders.paid,
                    orders.delivered
                FROM
                    orders JOIN order_item ON orders.id = order_item.order_id
                WHERE 
                    user_id={user_id} AND paid={paid};"""
        products = self.curr.execute(query).fetchall()
        return products

    def delete(self, pk):
        query = f"DELETE FROM orders WHERE id = ?;"
        try:
            with self.conn:
                self.curr.execute(query, (pk,))
                logging.info(f"Successfully deleted order with id {pk}")
        except Exception as e:
            logging.error(f"Error deleting data: {e}")


class OrderItemDB(Model):
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS order_item (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    order_id INTEGER NOT NULL,
                    count INTEGER NOT NULL,
                    FOREIGN KEY(order_id) REFERENCES orders(id));"""
        try:
            with self.conn:
                self.curr.execute(query)
                logging.info("Successfully created `order_item` table")
        except Exception as e:
            logging.error(f"Error creating table: {e}")

    def save(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO order_item ({columns}) VALUES ({placeholders});"
        try:
            with self.conn:
                self.curr.execute(query, values)
                logging.info(f"Successfully saved `order_item` table: {kwargs}")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def delete(self, pk):
        query = f"DELETE FROM order_item WHERE id = ?;"
        try:
            with self.conn:
                self.curr.execute(query, (pk,))
                logging.info(f"Successfully deleted order item with id {pk}")
        except Exception as e:
            logging.error(f"Error deleting data: {e}")


if __name__ == '__main__':
    UserDB()
    ProductDB()
    OrderDB()
    OrderItemDB()

    # ProductDB().save(name='Kartoshkali somsa', price=5000,
    #                  picture=ProductDB().bimg(img_path=f'{BASE_DIR}/media/taomlar/somsa.jpg'))

    # ProductDB().save(name='Tovuqli somsa', price=6000,
    #                  picture=ProductDB().bimg(img_path=f'{BASE_DIR}/media/taomlar/tovuqli_somsa.jpeg'))
    #
    # ProductDB().save(name='Go`shtli somsa', price=8000,
    #                  picture=ProductDB().bimg(img_path=f'{BASE_DIR}/media/taomlar/goshtli_somsa.jpeg'))

    # ProductDB().save(name='Kosa somsa', price=25000,
    #                  picture=ProductDB().bimg(img_path=f'{BASE_DIR}/media/taomlar/kosa_somsa.jpeg'))
