//用来寻找我们需要的数据,用眼睛看会看花的
var a="jNTk85TJlRgOjMN%2FVSsKu971r4nZJJg6Lx5XvHkc2wne1XnB3KvgQNXPGifdrq4ngRU6XigFBnFv%0Anyeh5%2F4pzlE9rKRZk0KrjrM5ZUnqkL6hwRuTlkes1lbZ9YOeJ2CAjX%2FTgPdVA7m0wTJxBFqkSEO0%0AAE%2FKNaa01QP2k7aHG9F5OldQQH0tzVDMgfNIb5Jkx37w2rXXlCnKe%2BgFdBEGxwBfzy4VuQGVhbwQ%0AxJ%2FgIC28mj1pPLbasSfQpxO3JXz9DA9a0uX9ZhgDZ3Cdmx9Gj%2BkhaOx62Y2HTJCQnxLwQaVlWWyM%0AYO%2FKZw%3D%3D|预订|5u000G13880A|G1388|NXG|AOH|NXG|AOH|15:53|19:42|03:49|Y|TwHFuS6zvn8mpm0uKr4cHiXgPSMaf5ZIKZ8AQ9juOsUMFn3D|20200412|3|G1|01|09|1|0|||||||||||11|8|2||O0M090|OM9|1|0|||||||||"
var b="|列车停运|6c000G130407|G1304|IZQ|AOH|NXG|AOH|24:00|24:00|99:59|IS_TIME_NOT_BUY||20200412||Q7|09|16|0|1|||||||||||||||||0|0|null||||||||"

var arr=a.split('|');
var newArr = []
for(let i=0;i<arr.length;i++){
    newArr[i]=i+' : '+arr[i]
}
console.log(newArr)