# djangorestframework-admin

## 介绍
基于DRF开发的后台管理

## 原则
### 模块依赖

### 搜索限制
1. 被依赖对象不能根据依赖对象过滤
   比如角色依赖用户，那用户就不能根据角色进行搜索；
2. 


## 软件架构
软件架构说明
* auth，身份认证与管理模块
  * user，用户管理
  * role，角色管理
  * permission，权限管理（RBAC模型）
* plugins，插件
  * jwt，基于JWT的登录与校验
  * model，基于models.Model的登录
* static，静态资源
  * swagger-ui，swagger文档的静态资源
* system，系统配置管理模块

## 使用
1. 新建DRF项目（以`backend`为例）；
2. 安装
3. 重置配置文件
```shell
cd backend/backend
mv settings.py default_settings.py
cp .../rest_framework_admin/template/settings.py ./
cp .../rest_framework_admin/template/urls.py ./
```
4. 更新需要
方法
