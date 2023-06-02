def ShowData():
    pageNum = int(request.args.get("pageNum"))
    pageSize = int(request.args.get("pageSize"))
    data_list = []
    all = query()
    for res in all:
        datas = {
            "id": res.id,
            "name": res.name,
            "age": res.age
        }
        data_list.append(datas)
    info = {"code": 0, "message": "OK", "total": len(data_list), "data": data_list[(pageNum - 1) * pageSize:pageNum * pageSize]}
    print(info)
    return info