curl --request POST \
  --url http://0.0.0.0:8080/textresponse/new \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form 'text=Do not eat here. Their food is stupid good. You'\''ll go broke due to not wanting to ever eat anywhere else. '


curl --request POST \
  --url http://0.0.0.0:8080/textresponse/new \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form 'text=this makes me really happy. '

curl --request POST \
  --url http://0.0.0.0:8080/emojiresponse/new \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form 'text=This makes me really sad. '
