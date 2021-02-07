# insta-auto

> Automate management instagram

### Definitions

- `Reactions` - List of reaction(like, comment, follow) from each post
- `Jobs` - Daliy waitlist for What i want to do.
- `Crawler` - Scrap reactions from instagram posts and convert `Reactions` to `Jobs`
- `Reactor` - Consume and work job from `Jobs`
- `Panel` - Convert `Jobs` to **Template(web)** and **Template** to `Jobs`

### Goal

Management instagram more easily

### Architectrue


- | Insta | --> Reactions --> `Crawler` --> Jobs --> | DB |
- | DB | --> Jobs --> `Panel` --> Template(form) --> | User |
- | DB | <-- Jobs <-- `Panel` <-- Template(Actions) <-- | User |
- | Insta | <-- Jobs <-- `Reactor` <-- Jobs <-- | DB |


### Data structure
- Reactions:
```
    - Reactions(user type): {
        follower: {
            user_name: String,
            is_following: Boolean,
            follower: Number,
            following: Number,
            top_three_posts: [ 
                post: {
                    link: String
                    liked(좋아요 여부): Boolean
                }... 
            ]
        }
    }

    - Reactions(post type): { 
        post_name(link): String,
        react_users:{
            user_name: {
                react_type: Number(none: 0, like:1, comment:2),
                comments: [ String ]
            }
        }
    }...
```

 - Jobs

상호작용은 2개로 나누어지는데, 유저-내 포스트와 유저-나 다.

상태는 따로 나누지않고 버튼의 색으로 표시한다.
  ```
    - Jobs(each post - N:N): {
        user_name(link): String,
        comment: [ String ],
    }
    - Jobs(each user - 1:N): {
        react_type: Number(none: 0, follow: 1, like(reflect): 2),
    }
  ```
  
  ### Demo
  [demo](#)

## 리팩토링 리스트

### 1. 크롤러

- [ ] 크롤러 세팅 값 로드 - 옵저블 객체 등록
- [ ] 브라우저 세팅
- [ ] 팔로워에서 리액션 추출(유저리스트)
- [ ] 유저리스트에서 탑3 추출
- [ ] 내 포스트에서 리액션 추출
- [x] DB 저장할 데이터 ORM 매핑 준비(관계 명시)
- [ ] 

### 2. 리액터