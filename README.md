Football Data Pipeline

This is a simple Data Enginner Project.
By following this pipeline

Football API  
   ↓  
Python script (EC2)  
   ↓  
S3 (raw)  
   ↓  
PostgreSQL (RDS or local)

Setup
1. Create a AWS EC2 virtual server
2. Create S3 bucket and RDS database
3. Connect S3 and RDS with EC2
4. Install python dependencies
5. Add environment variables including FOOTBALL_API_TOKEN, PG_HOST, PG_DB, PG_USER, PG_PASSWORD
6. Run fetch_football.py
