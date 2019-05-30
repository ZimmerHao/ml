## 创建 k8s role

```
curl -X POST \
  http://192.168.60.10:8000/dashboard/k8s/roles/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 50be9ce5-b337-44d3-b1a4-b70be23aef16' \
  -H 'cache-control: no-cache' \
  -d '{
	"name": "aaaa",
	"namespace": "aaa",
	"resource_id": 1,
	"verbs": ["list"]
}'
```

## k8s role 详情

```
curl -X GET \
  http://192.168.60.10:8000/dashboard/k8s/roles/1/ \
  -H 'Postman-Token: d20b9166-d247-446b-8562-1806948631c5' \
  -H 'cache-control: no-cache'
```

## k8s role 列表

```
curl -X GET \
  http://192.168.60.10:8000/dashboard/k8s/roles/ \
  -H 'Postman-Token: 2c7d12b1-3789-4f66-952e-458f27909ea0' \
  -H 'cache-control: no-cache'
  
[
    {
        "id": 1,
        "date_added": "2019-05-25T14:03:50.312602Z",
        "date_updated": "2019-05-25T14:03:50.323214Z",
        "name": "aaaa",
        "namespace": "aaa",
        "verbs": [
            "list"
        ],
        "is_active": true,
        "k8s_resources": [
            1
        ]
    }
]  

```

## 更新 k8s role

```

curl -X PUT \
  http://192.168.60.10:8000/dashboard/k8s/roles/1/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 8b0216eb-c9fd-46ee-b6ac-d8efc4e793ce' \
  -H 'cache-control: no-cache' \
  -d '{
	"verbs": ["list", "get"]
}'

{
    "id": 1,
    "date_added": "2019-05-25T14:03:50.312602Z",
    "date_updated": "2019-05-25T14:38:37.937328Z",
    "name": "aaaa",
    "namespace": "aaa",
    "verbs": [
        "list",
        "get"
    ],
    "is_active": true,
    "k8s_resources": [
        1
    ]
}
```

## 注册

```
curl -X POST \
  http://192.168.60.10:8000/api/v1/users/signup/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 491d5608-aa8b-41c1-aadc-d1a837f99d2c' \
  -H 'cache-control: no-cache' \
  -d '{
	"account": "526662774@qq.com",
	"password": "123456"
}'

```

## 登录

```

curl -X POST \
  http://192.168.60.10:8000/api/v1/users/login/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 1e7237c2-cee4-493d-80a9-a9c41c1cfde6' \
  -H 'X-CSRFToken: 07C6pFXg8nwkpjeSztxtWAvCue57HVOjIrFHRz3U9IIWRkvgddTSoKUldtowwGHd' \
  -H 'cache-control: no-cache' \
  -d '{
	"account": "526662774@qq.com",
	"password": "123456"
}'


{
    "id": 1,
    "date_added": "2019-05-25T14:45:58.545025Z",
    "date_updated": "2019-05-25T14:45:58.545047Z",
    "password": "pbkdf2_sha256$120000$8jPt3QpWjiRk$Ek71QSLYq4eU/j5zADZE7P2cRANeUg9vpRQF6tTTS4o=",
    "last_login": "2019-05-25T15:13:42.375877Z",
    "nickname": "Thadasime",
    "avatar": "",
    "email": "526662774@qq.com",
    "country": "",
    "is_staff": false,
    "is_superuser": false,
    "is_active": true,
    "k8s_roles": []
}


```

## 登出

```
curl -X POST \
  http://192.168.60.10:8000/api/v1/users/logout/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: e1c302ba-a7f7-4c11-9c8e-7e4a344b8d4a' \
  -H 'X-CSRFToken: 07C6pFXg8nwkpjeSztxtWAvCue57HVOjIrFHRz3U9IIWRkvgddTSoKUldtowwGHd' \
  -H 'cache-control: no-cache'
```

## 用户分配k8s role

```
curl -X POST \
  http://192.168.60.10:8000/dashboard/users/1/k8s/roles/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: be2f6354-b0a2-4cbe-92e4-0adadb6df6b1' \
  -H 'X-CSRFToken: a2l4ooBZ6ag6S8Y4HjCDgJg7K1PV1fFSyrr7Uc1QzpP0bAmTS0WlKOy3XGFtleuu' \
  -H 'cache-control: no-cache' \
  -d '{
	"k8s_role_id": 1
}'

{
    "id": 1,
    "date_added": "2019-05-25T14:45:58.545025Z",
    "date_updated": "2019-05-26T10:51:41.263270Z",
    "last_login": "2019-05-26T09:37:19.832290Z",
    "nickname": "Thadasime",
    "avatar": "",
    "email": "526662774@qq.com",
    "country": "",
    "is_active": true,
    "k8s_roles": [
        1
    ]
}
```

## 用户的k8s role

```
curl -X GET \
  http://192.168.60.10:8000/dashboard/users/1/k8s/roles/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 3e7f9206-c32e-468a-bc91-8b3d8a7ded3a' \
  -H 'X-CSRFToken: a2l4ooBZ6ag6S8Y4HjCDgJg7K1PV1fFSyrr7Uc1QzpP0bAmTS0WlKOy3XGFtleuu' \
  -H 'cache-control: no-cache' \
  -d '{
	"k8s_role_id": 1
}'

{
    "id": 1,
    "date_added": "2019-05-25T14:45:58.545025Z",
    "date_updated": "2019-05-26T10:54:58.224504Z",
    "last_login": "2019-05-26T09:37:19.832290Z",
    "nickname": "Thadasime",
    "avatar": "",
    "email": "526662774@qq.com",
    "country": "",
    "is_active": true,
    "k8s_roles": [
        1
    ]
}

```

## 删除用户的k8s role

```
curl -X DELETE \
  http://192.168.60.10:8000/dashboard/users/1/k8s/roles/ \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: ed4e9fc0-6cb1-4b11-9766-f29bd562433c' \
  -H 'X-CSRFToken: a2l4ooBZ6ag6S8Y4HjCDgJg7K1PV1fFSyrr7Uc1QzpP0bAmTS0WlKOy3XGFtleuu' \
  -H 'cache-control: no-cache' \
  -d '{
	"k8s_role_id": 1
}'

{
    "id": 1,
    "date_added": "2019-05-25T14:45:58.545025Z",
    "date_updated": "2019-05-26T10:51:52.935923Z",
    "last_login": "2019-05-26T09:37:19.832290Z",
    "nickname": "Thadasime",
    "avatar": "",
    "email": "526662774@qq.com",
    "country": "",
    "is_active": true,
    "k8s_roles": []
}
```

