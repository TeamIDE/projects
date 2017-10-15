# PROJECTS

This micro service will handle the projects endpoint. The feature list is as follow:

 * GET a list of all projects
 * GET a specific project by id
 * POST a new project
 * POST a list of projects

GET (* indicates optional)
```
http://domain.com/projects?id*
```

POST (*indicates optional)
```json
{
id : string,
title : string
}
```
