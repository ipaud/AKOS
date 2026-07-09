# Examples — REST Pack

## Resource + verb, not verb-in-URL

Bad: `POST /createOrder`, `POST /getOrderById`
Good: `POST /orders`, `GET /orders/:id`

## Consistent envelope

```json
{ "data": { "id": "123", "name": "..." }, "meta": { "requestId": "..." } }
```
Errors: `{ "error": { "code": "ORDER_NOT_FOUND", "message": "Order 123 not found" } }`

## Cursor pagination

```
GET /orders?cursor=eyJpZCI6MTIzfQ&limit=20
→ { "data": [...], "nextCursor": "eyJpZCI6MTQzfQ" }
```

## Versioned breaking change

`/v1/orders` returns `{ total: number }`; `/v2/orders` changes it to `{ totalCents: number }` — both served concurrently during the deprecation window, `/v1` sunset date announced.
