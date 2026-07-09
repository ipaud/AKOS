# Examples — GraphQL Pack

## N+1 fix with DataLoader

Bad:

```js
const resolvers = {
  Order: { customer: (order) => db.customers.findOne(order.customerId) } // one query per order
};
```

Good:

```js
const customerLoader = new DataLoader(ids => db.customers.findMany({ id: { in: ids } }));
const resolvers = {
  Order: { customer: (order) => customerLoader.load(order.customerId) } // batched into one query
};
```

## Field-level authorization

```js
const resolvers = {
  User: {
    email: (user, args, ctx) => ctx.user.id === user.id || ctx.user.role === 'admin' ? user.email : null,
  }
};
```

## Query depth limiting

```js
const server = new ApolloServer({
  validationRules: [depthLimit(5)], // reject queries nested deeper than 5
});
```

## Deprecated field

```graphql
type User {
  fullName: String @deprecated(reason: "Use firstName and lastName instead")
  firstName: String
  lastName: String
}
```
