from app import app
c = app.test_client()
paths = ["/", "/projects", "/contact", "/static/style.css", "/static/script.js", "/static/IMG_1774.jpeg"]
for p in paths:
    r = c.get(p)
    print(p, r.status_code)
r = c.post("/contact", data={"name":"Test","email":"a@b.c","message":"Hi"}, follow_redirects=False)
print("POST /contact", r.status_code, r.headers.get("Location"))
