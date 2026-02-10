# 🧠 Project Learnings & Developer Notes
## How to Verify Data in the Database
### Enter the Database Container:`

```bash
docker exec -it rag_assistant_db psql -U rag_user -d rag_db
```

### List all Users
```sql
SELECT * FROM users;
```

### List all Queries
```sql
SELECT * FROM queries;
```
*Exit: Type `\q` to exit the database.*