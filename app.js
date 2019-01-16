new Vue({
	el:"#vue-app",
	data:
	{	
		length:100,
		flag:false
		
	},
	methods:
	{
		res:function()
		{
			this.length=100;
			this.flag=false;
		},
		hit:function()
		{
			this.length-=10;
			if(this.length<=0)this.flag=true;
		}
		
	}
	  
});
