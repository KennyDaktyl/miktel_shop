const order_id=$('#order_id').val();const domain=location.protocol+'//'+location.host+'/zamowienie_zakonczono/'+order_id;var PAYMENT_INTENT_CLIENT_SECRET=$('#p_i_sec').val();var PUBLIC_KEY=$('#public_key').val();var stripe=Stripe(PUBLIC_KEY);var elements=stripe.elements();var options={style:{base:{padding:'10px 12px',color:'#32325d',fontSize:'16px','::placeholder':{color:'#aab7c4'},},},};var p24Bank=elements.create('p24Bank',options);p24Bank.mount('#p24-bank-element');var form=document.getElementById('payment-form');var accountholderName=document.getElementById('accountholder-name');var accountholderEmail=document.getElementById('accountholder-email');form.addEventListener('submit',function(event){event.preventDefault();stripe.confirmP24Payment(PAYMENT_INTENT_CLIENT_SECRET,{payment_method:{p24:p24Bank,billing_details:{name:accountholderName.value,email:accountholderEmail.value,},},payment_method_options:{p24:{}},return_url:domain,});});