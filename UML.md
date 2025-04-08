# 🧩 UML Class Diagram — Storage Project

```markdown
+-------------------+
|     Product       |
+-------------------+
| id                |
| name              |
| barcode           |
| category          |
| is_edible         |
| default_image     |
+-------------------+
|                   |
+-------------------+
         |
         | 1
         | 
         | ∞
+-----------------------+
|     ProductBatch      |
+-----------------------+
| id                    |
| product_id (FK)       |
| expiration_date       |
| size_volume           |
| quantity              |
| purchase_price        |
| sale_price_per_item   |
| wholeprice            |
| discount              |
| income_date           |
| outgoing_date         |
| location_id (FK)      |
| accumulated_price     |
| nutrition_id (FK)     |
+-----------------------+

+-------------------------+
|     NutritionData       |
+-------------------------+
| id                      |
| per_serving_calories    |
| per_serving_fat         |
| per_serving_carbs       |
| per_serving_protein     |
| per_whole_calories      |
| per_whole_fat           |
| per_whole_carbs         |
| per_whole_protein       |
| serving_size            |
+-------------------------+

+------------------------+
|    LocationFinder      |
+------------------------+
| id                     |
| name                   |
| type (City, WH, etc.)  |
| code                   |
| description            |
| parent_id (FK)         |
+------------------------+

+------------------------+
|     ProductImage       |
+------------------------+
| id                     |
| product_id (FK)        |
| image_file             |
+------------------------+
```