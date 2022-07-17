# Load environment variables into a monorepo from a `toml`-file

Sometimes it can be beneficial to have environment-files (`*.env`) at different levels in your monorepo.

To motivate this thought I'll go through a short example. 

## Example

Say you are launching a `Next JS` application using both a `docker-compose.yml`-config at the root of the repo, and a separate command at the applications folder. This could typically happen if you would want to run `yarn dev` inside the application folder, in addition to being able to launch the whole stack using `docker compose`.

```markdown
docker-compose.yml
.env

web/
    services/
        app/
            .env.local
        other-app/
            .env
```

In this case you would need to define the environment variables for all your applications one by one, unlike when using only `docker compose`. This is especially bothersome once the number of applications inside your monorepo grows.

To ease the process of onboarding new developers (reducing the number of `.env`-files to set up) it would therefore be beneficial to only require one file. My solution to this problem is then using a single `.toml`-file to define the hierarchy of environment variables.

```toml
[".env"]
  SECRET="hush"
[web]
  [web.services]
    [web.services.app] 
      [web.services.app.".env.local"] 
        SECRET="top-secret"
        TOKEN="shhh"
    [web.services.other-app] 
      [web.services.other-app.".env"] 
        AREA_52="tonopah-test-range"
```