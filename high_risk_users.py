import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute("""

select
    u.user_name,
    o.billing_email,
    count(*) as total_orders,
    sum(
        case
            when o.amount >= 100000 then 1
            else 0
        end
    ) as high_risk_orders,
    sum(o.amount) as total_amount
from 
    orders as o
join
    users as u
on
    o.billing_email = u.billing_email
group by
    o.billing_email
having
    sum(o.amount) > (
                select
                    avg(total_amount)
                from (
                    select 
                        billing_email,
                        sum(o2.amount) as total_amount
                    from 
                        orders as o2
                    group by 
                          billing_email
                    ) as user_totals
                ) and 
                     sum(
                        case
                            when o.amount >= 100000 then 1
                            else 0
                    end
            ) >= 2
               """)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
