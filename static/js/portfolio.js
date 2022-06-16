
function today_price_get_K(obj) {
  //해당 열 테이블 인덱스
  var Num = obj.parentNode.parentNode.rowIndex-1;
  
  //가격 input value
  var price = document.querySelector('#tbody_K > tr:nth-child('+(Num+1)+') > td:nth-child(5) > input');
  
  //--------------------------------------------------------//
  //종목코드 value 전처리
  const input_ticker = document.getElementsByName('ticker');
  //형변환(배열)
  const input_ticker_arr = Array.from(input_ticker)
  //값이 비어있는 인덱스 삭제
  const unnull_idx = []
  for(let i=0;i<input_ticker_arr.length;i++){
    if(input_ticker_arr[i].value=='') {
      //console.log('null 인덱스 : '+ i);
    }
    else{
      //console.log('unnull 인덱스 : '+ i);
      unnull_idx.push(i);
    }
  }
  const ticker = [];
  for(let j=0;j<unnull_idx.length;j++){
    ticker.push(input_ticker_arr[unnull_idx[j]].value);
  }
  const ticker_final = []
  for(let k=0;k<ticker.length;k++){
    ticker_final.push(ticker[k].split('|')[1].trim())
  }
  const ticker_K_final = [];
  const ticker_F_final = [];
  const pat = /[0-9]+/
  for(let h=0;h<ticker_final.length;h++){
    if(pat.test(ticker_final[h])==true){ticker_K_final.push(ticker_final[h])}
    else{ticker_F_final.push(ticker_final[h])}
  }
  console.log(ticker_K_final)
  console.log(ticker_F_final)
  //--------------------------------------------------------//
  //--------------------------------------------------------//
  const data_K_ticker = data['K_code'];
  const data_K_price = data['K_price'];
  //종목코드와 일치하는 가격 불러오기
  var price_fi = []
  for(let x=0;x<ticker_K_final.length;x++){
    var idx = data_K_ticker.indexOf(ticker_K_final[x]);
    price_fi.push(data_K_price[idx])
  }
  console.log(price_fi)
  //--------------------------------------------------------//
  //--------------------------------------------------------//
  //HTML에 입력
  price.value = price_fi[Num]
  console.log(Num)
  //--------------------------------------------------------//
}

function today_price_get_F(obj) {
  //해당 열 테이블 인덱스
  var Num = obj.parentNode.parentNode.rowIndex-1;
  
  //가격 input value
  var price = document.querySelector('#tbody_F > tr:nth-child('+(Num+1)+') > td:nth-child(5) > input');
  //--------------------------------------------------------//
  //종목코드 value 전처리
  const input_ticker = document.getElementsByName('ticker');
  //형변환(배열)
  const input_ticker_arr = Array.from(input_ticker)
  //값이 비어있는 인덱스 추출
  const unnull_idx = []
  for(let i=0;i<input_ticker_arr.length;i++){
    if(input_ticker_arr[i].value=='') {
      //console.log('null 인덱스 : '+ i)
    }
    else{
      //console.log('unnull 인덱스 : '+ i)
      unnull_idx.push(i);
    }
  }
  const ticker = [];
  for(let j=0;j<unnull_idx.length;j++){
    ticker.push(input_ticker_arr[unnull_idx[j]].value);
  }
  const ticker_final = []
  for(let k=0;k<ticker.length;k++){
    ticker_final.push(ticker[k].split('|')[1].trim())
  }
  const ticker_K_final = [];
  const ticker_F_final = [];
  const pat = /[0-9]+/
  for(let h=0;h<ticker_final.length;h++){
    if(pat.test(ticker_final[h])==true){ticker_K_final.push(ticker_final[h])}
    else{ticker_F_final.push(ticker_final[h])}
  }
  console.log(ticker_K_final)
  console.log(ticker_F_final)
  //--------------------------------------------------------//
  
  //--------------------------------------------------------//
  const data_F_ticker = data['F_code'];
  const data_F_price = data['F_price'];
  //종목코드와 일치하는 가격 불러오기
  var price_fi = []
  for(let x=0;x<ticker_F_final.length;x++){
    var idx = data_F_ticker.indexOf(ticker_F_final[x]);
    price_fi.push(data_F_price[idx])
  }
  console.log(price_fi)
  //--------------------------------------------------------//
  //--------------------------------------------------------//
  //HTML에 입력
  price.value = price_fi[Num]
  console.log(Num)
  //--------------------------------------------------------//
}

function today_price_add_get_K(obj) {
  //해당 열 테이블 인덱스
  var Num = obj.parentNode.parentNode.parentNode.rowIndex-1;
  
  //가격 input value
  var price = document.querySelector('#tbody_K > tr:nth-child('+(Num+1)+') > td:nth-child(5) > input');
  
  //--------------------------------------------------------//
  //종목코드 value 전처리
  const input_ticker = document.getElementsByName('ticker');
  //형변환(배열)
  const input_ticker_arr = Array.from(input_ticker)
  //값이 비어있는 인덱스 삭제
  const unnull_idx = []
  for(let i=0;i<input_ticker_arr.length;i++){
    if(input_ticker_arr[i].value=='') {
      //console.log('null 인덱스 : '+ i);
    }
    else{
      //console.log('unnull 인덱스 : '+ i);
      unnull_idx.push(i);
    }
  }
  const ticker = [];
  for(let j=0;j<unnull_idx.length;j++){
    ticker.push(input_ticker_arr[unnull_idx[j]].value);
  }
  const ticker_final = []
  for(let k=0;k<ticker.length;k++){
    ticker_final.push(ticker[k].split('|')[1].trim())
  }
  const ticker_K_final = [];
  const ticker_F_final = [];
  const pat = /[0-9]+/
  for(let h=0;h<ticker_final.length;h++){
    if(pat.test(ticker_final[h])==true){ticker_K_final.push(ticker_final[h])}
    else{ticker_F_final.push(ticker_final[h])}
  }
  console.log(ticker_K_final)
  console.log(ticker_F_final)
  //--------------------------------------------------------//
  //--------------------------------------------------------//
  const data_K_ticker = data['K_code'];
  const data_K_price = data['K_price'];
  //종목코드와 일치하는 가격 불러오기
  var price_fi = []
  for(let x=0;x<ticker_K_final.length;x++){
    var idx = data_K_ticker.indexOf(ticker_K_final[x]);
    price_fi.push(data_K_price[idx])
  }
  console.log(price_fi)
  //--------------------------------------------------------//
  //--------------------------------------------------------//
  //HTML에 입력
  price.value = price_fi[Num]
  console.log(Num)
  //--------------------------------------------------------//
}

function today_price_add_get_F(obj) {
  var Num = obj.parentNode.parentNode.parentNode.rowIndex-1;
  
  //가격 input value
  var price = document.querySelector('#tbody_F > tr:nth-child('+(Num+1)+') > td:nth-child(5) > input');
  //--------------------------------------------------------//
  //종목코드 value 전처리
  const input_ticker = document.getElementsByName('ticker');
  //형변환(배열)
  const input_ticker_arr = Array.from(input_ticker)
  //값이 비어있는 인덱스 추출
  const unnull_idx = []
  for(let i=0;i<input_ticker_arr.length;i++){
    if(input_ticker_arr[i].value=='') {
      //console.log('null 인덱스 : '+ i)
    }
    else{
      //console.log('unnull 인덱스 : '+ i)
      unnull_idx.push(i);
    }
  }
  const ticker = [];
  for(let j=0;j<unnull_idx.length;j++){
    ticker.push(input_ticker_arr[unnull_idx[j]].value);
  }
  const ticker_final = []
  for(let k=0;k<ticker.length;k++){
    ticker_final.push(ticker[k].split('|')[1].trim())
  }
  const ticker_K_final = [];
  const ticker_F_final = [];
  const pat = /[0-9]+/
  for(let h=0;h<ticker_final.length;h++){
    if(pat.test(ticker_final[h])==true){ticker_K_final.push(ticker_final[h])}
    else{ticker_F_final.push(ticker_final[h])}
  }
  console.log(ticker_K_final)
  console.log(ticker_F_final)
  //--------------------------------------------------------//
  
  //--------------------------------------------------------//
  const data_F_ticker = data['F_code'];
  const data_F_price = data['F_price'];
  //종목코드와 일치하는 가격 불러오기
  var price_fi = []
  for(let x=0;x<ticker_F_final.length;x++){
    var idx = data_F_ticker.indexOf(ticker_F_final[x]);
    price_fi.push(data_F_price[idx])
  }
  console.log(price_fi)
  //--------------------------------------------------------//
  //--------------------------------------------------------//
  //HTML에 입력
  price.value = price_fi[Num]
  console.log(Num)
  //--------------------------------------------------------//
}

function ADDRow_K() {
  var No_K = 2
  var cnt = 2;
  var tbody_K = document.getElementById('tbody_K');
  var row = tbody_K.insertRow(tbody_K.rows.length); // 하단에 추가
  var cell0 = row.insertCell(0);
  var cell1 = row.insertCell(1);
  var cell2 = row.insertCell(2);
  var cell3 = row.insertCell(3);
  var cell4 = row.insertCell(4);
  var cell5 = row.insertCell(5);
  var cell6 = row.insertCell(6);
  
  cell0.innerHTML = '<center><strong>'+No_K+'<strong></center>';
  cell1.innerHTML = '<input class="btn btn-outline-dark btn-sm" aria-label="Default select example" type="text" list="list_K" name="ticker"/><datalist class="ticker'+cnt+'" id ="list_K"></datalist>';
  for(let i = 0; i<data['K_company'].length; i++){
    var ticker_datalist = document.querySelector(".ticker"+cnt)
    var option = document.createElement('option');
    var text = document.createTextNode(data['K_company']+data['K_code'][i]);
    option.appendChild(text);
    ticker_datalist.appendChild(option);
  }
  cnt++;
  
  cell2.innerHTML = '<select class="btn btn-outline-dark btn-sm" aria-label="Default select example" name="order_state"><option selected>매수</option><option value="매도">매도</option><option value="예약">예약</option></select>';
  cell3.innerHTML = '<input class="rounded-3 border-1 btn-outline-dark" type="text" size="15" name="stock_cnt">';
  cell4.innerHTML = '<input class="rounded-3 border-1 btn-outline-dark" type="text" size="15" name="price">';
  cell5.innerHTML = '<center><input type="button" value="현재 주가로" class="btn btn-outline-success btn-sm" onclick=\'today_price_add_get_K(this);\'></center>';
  cell6.innerHTML = '<center><input type="button" value="한 줄 삭제" class="btn btn-outline-danger btn-sm" name="clear_row" onclick=\'clear_row_del(this);\'></center>';
  No_K++;
}

function ADDRow_F() {
  var No_F = 2;
  var cnt = 2;
  var tbody_F = document.getElementById('tbody_F');
  var row = tbody_F.insertRow(tbody_F.rows.length); // 하단에 추가
  var cell0 = row.insertCell(0);
  var cell1 = row.insertCell(1);
  var cell2 = row.insertCell(2);
  var cell3 = row.insertCell(3);
  var cell4 = row.insertCell(4);
  var cell5 = row.insertCell(5);
  var cell6 = row.insertCell(6);
  
  cell0.innerHTML = '<center><strong>'+No_F+'<strong></center>';
  cell1.innerHTML = '<input class="btn btn-outline-dark btn-sm" aria-label="Default select example" type="text" list="list_F" name="ticker"/><datalist class="ticker'+cnt+'" id ="list_F"></datalist>';
  for(let i = 0; i<data['F_company'].length; i++){
    var ticker_datalist = document.querySelector(".ticker"+cnt)
    var option = document.createElement('option');
    var text = document.createTextNode(data['F_company']+data['F_code'][i]);
    option.appendChild(text);
    ticker_datalist.appendChild(option);
  }
  cnt++;
  
  cell2.innerHTML = '<select class="btn btn-outline-dark btn-sm" aria-label="Default select example" name="order_state"><option selected>매수</option><option value="매도">매도</option><option value="예약">예약</option></select>';
  cell3.innerHTML = '<input class="rounded-3 border-1 btn-outline-dark" type="text" size="15" name="stock_cnt">';
  cell4.innerHTML = '<input class="rounded-3 border-1 btn-outline-dark" type="text" size="15" name="price">';
  cell5.innerHTML = '<center><input type="button" value="현재 주가로" class="btn btn-outline-success btn-sm" onclick=\'today_price_add_get_F(this);\'></center>';
  cell6.innerHTML = '<center><input type="button" value="한 줄 삭제" class="btn btn-outline-danger btn-sm" name="clear_row" onclick=\'clear_row_del(this);\'></center>';
  No_F++;
}

function clear_row_del(obj) {
  if (No_K==1){
    alert('더이상 지울 수 없습니다.');
    history.back(-1);
  } else{
    var tr = obj.parentNode.parentNode;
    tr.parentNode.remove(tr);
    No_K -=1;
  }
  cnt -=1;
}

var prices = document.getElementsByClassName('ticker')
for(var i=0;i<prices.length;i++){
  console.log(prices.item(i).value)
}

console.log()