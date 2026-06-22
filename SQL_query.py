import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute("""

select
    u.user_name,
    o.billing_email,
    p.payment_method,
    p.card_brand,
    count(*) as total_orders,
    sum(
        case
            when o.amount >= 200000 then 1
            else 0
        end
    ) as high_amount_orders,
    sum(o.amount) as total_amount
from
    orders as o
join
     users as u
on
    o.billing_email = u.billing_email
join 
    payments as p
on 
    u.billing_email = p.billing_email
group by
    o.billing_email
having
    sum(o.amount) > (
        select 
            avg(total_amount)
        from (
                select
                    o3.billing_email,
                    sum(o3.amount) as total_amount
                from 
                    orders as o3
                group by 
                    o3.billing_email) as user_totals)
                    and
                sum(
                    case
                        when o.amount >= 200000 then 1
                    else 0
                end) >= 1  
order by
    sum(o.amount) DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
