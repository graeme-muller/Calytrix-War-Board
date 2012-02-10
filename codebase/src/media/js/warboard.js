var WarBoard = {
	Panels:{
		ProjectStatus:{'panel-class':'project-panel',
					   'opts':{'urls':
					  			{
						  			'greenhopper:project_progress':'/jira/greenhopper/project_progress',
						  			'greenhopper:days_remaining'  :'/jira/greenhopper/days_remaining'
					  		    }
					         }
					  },
		MadFlipper:{ 'panel-class':'madflipper-panel',
					 'opts':{}
				   },
		Nothing:{ 'panel-class':'nothing-panel',
				  'opts':{}
				}
	},
	doLayout: function(){
				// grab the window
				var theWindow = jQuery(window);
				var screenWidth = theWindow.width();
				var screenHeight = theWindow.height();
				// grab the flip panels
				var flipPanels = jQuery('.flipPanel');
				// work out the padding and margin being applied to
				// the sides so we can figure out sizes properly
				var padding = {};
				var margin = {};
				var sides = ['top', 'right', 'bottom', 'left'];
				for(var i=0; i<sides.length; i++)
				{
					var sidePadding = flipPanels.css('padding-'+sides[i]);
					sidePadding = parseInt(sidePadding==""?"0":sidePadding);
					padding[sides[i]] = sidePadding;
					var sideMargin = flipPanels.css('margin-'+sides[i]);
					sideMargin = parseInt(sideMargin==""?"0":sideMargin);
					margin[sides[i]] = sideMargin;
				}

				// figure out how much spacing to allow when calculating
				// widths of panels in relation to the available screen area
				var totalHeightPadding = ( margin.top + margin.bottom + padding.top + padding.bottom ) * 3;
				var totalWidthPadding  = ( margin.left + margin.right + padding.left + padding.right ) * 3;
				var hGap = Math.round( screenWidth / 100 );
				var vGap = Math.round( screenHeight / 100 );
				var totalHgap = hGap * 4;
				var totalVgap = vGap * 4;

				// work out the final widths
				var flipWidth = (Math.round( ( screenWidth-totalWidthPadding-totalHgap ) / 3) )+ 'px';
				var flipHeight = (Math.round( (screenHeight-totalHeightPadding-totalVgap) / 3) )+ 'px';

				jQuery('body').css({ 'margin-left': Math.round(screenWidth / 100) + 'px'});
				jQuery('.flipPanel').each(function(idx, elm){
					jQuery(this).css({ 'width':flipWidth,
					                   'height':flipHeight });
				});
	},
	/**
	 * Trigger the animation to hide the panel
	 * @param jQcell the jQuery elementwhich contains the panel
	 * @returns nothing
	 */
	flipout: function( jQcell ){
		jQcell.removeClass('flipInY').addClass('flipOutY');
	},
	/**
	 * Trigger the animation to show the panel
	 * @param jQcell the jQuery elementwhich contains the panel
	 * @returns nothing
	 */
	flipin: function ( jQcell ){
		jQcell.removeClass('flipOutY').addClass('flipInY');
	},
	/**
	 * Assigns a flip panel a warboard panel class, removing any other
	 * warboard panel classes beforehand. See PanelClasses
	 */
	assignPanelClass: function(  jQcell, panelType )
	{
		for(key in WarBoard.Panels )
		{
			jQcell.removeClass( WarBoard.Panels[key]['panel-class'] );
		}
		jQcell.addClass( panelType['panel-class'] )
	},

	/*********************************************************************************************\
	|                                                                                             |
	|                                              PANELS                                         |
	|                                                                                             |
	\*********************************************************************************************/
	//=============================================================================================
	// PROJECT STATUS PANEL
	//=============================================================================================
	ProjectStatusPanel: {
		/**
		 * Create a project status panel
		 * @param jQcell the jQuery elementwhich contains the panel
		 * @param projectID the JIRA ID of the project to put in the panel
		 * @returns nothing
		 */
		init:function( jQcell, projectID ) {
			// This is a Project Panel
			var panelType = WarBoard.Panels.ProjectStatus;
			var daysRemainingURL = panelType.opts.urls['greenhopper:days_remaining'];
			var projectProgressURL = panelType.opts.urls['greenhopper:project_progress'];

			// first hide the panel
			WarBoard.flipout( jQcell );

			// set up the panel as a project panel
			WarBoard.assignPanelClass( jQcell, panelType );

			// obtain the data for the cell
			jQuery.ajax({
				type:'GET',
				url:daysRemainingURL,
				data:{ 'projectId': projectID,
					 },
				dataType:'json',
				success: function( json ){
					var html = '<div class="name">'+ json.project.name + '</div>';
					html +=    '<div class="version">' + json.version.name +'</div>'
					html +=    '<div class="days_remaining">' + json.version.daysRemaining +'</div>'
					jQcell.html( html );

					jQuery.ajax({
						type:'GET',
						url:projectProgressURL,
						data:{ 'selectedProjectId': projectID,
							 },
						dataType:'json',
						success: function( json ){
							var barItems = json.progressStatsList[0].progressStats.barItems;
							var offsets = [0];
							var offset = 0;
							for(var i=0; i<barItems.length;i++)
							{
								var barValue = parseInt(barItems[i].ratio);
								offset += barValue;
								offsets.push( offset-1 )
								offsets.push( offset )
							}

							var rgb = [ [255,0,0], [255,0,0], [255,255,0], [255,255,0], [0,255,0], [0,255,0], [0,255,0] ];
							var FFgradient = "-moz-linear-gradient(bottom";
							var WKgradient = "-webkit-gradient(linear, left bottom, left top";
							for(var i=0; i<offsets.length; i++)
							{
								FFgradient += ", rgba("+rgb[i][0]+","+rgb[i][1]+","+rgb[i][2]+",1) "+offsets[i]+"%"
								WKgradient += ", color-stop("+offsets[i]+"%,rgba("+rgb[i][0]+","+rgb[i][1]+","+rgb[i][2]+",1))"
							}
							FFgradient+=")";
							WKgradient+=")";

							jQcell.css({background:FFgradient});
							jQcell.css({background:WKgradient});

							// finally, show the panel now that it's ready
							WarBoard.flipin( jQcell );
						},
						error: function( jqXHR, textStatus, errorThrown )
						{
							console.log( 'ERROR!', jqXHR, errorThrown );
							// finally, show the panel now that it's ready
							WarBoard.flipin( jQcell );
						}
					});

				},
				error: function( jqXHR, textStatus, errorThrown )
				{
					console.log( 'ERROR!', jqXHR, errorThrown );
							// finally, show the panel now that it's ready
							WarBoard.flipin( jQcell );
				}
			});
		},
		destroy:function( jQcell ) {
			// nothing to see here
		}
	},
	//=============================================================================================
	// MAD FLIPPER PANEL
	//=============================================================================================
	/**
	 * Create a mad flipper panel
	 * @param jQcell the jQuery elementwhich contains the panel
	 * @returns nothing
	 */
	MadFlipperPanel: {
		randomPhrases:[ '<p>Is the Space Pope reptilian!? One hundred dollars. Or a guy who burns down a bar for the insurance money! WINDMILLS DO NOT WORK THAT WAY! GOOD NIGHT! Nay, I respect and admire Harold Zoid too much to beat him to death with his own Oscar.</p> <p>That could be \'my\' beautiful soul sitting naked on a couch. If I could just learn to play this stupid thing. I daresay that Fry has discovered the smelliest object in the known universe! Take me to your leader! You\'re going to do his laundry? Oh yeah, good luck with that.</p>',
					    '<p>Can\'t you people take the law into your own hands? I mean, we can\'t be policing the entire city! No children have ever meddled with the Republican Party and lived to tell about it. Aaah! Natural light! Get it off me! Get it off me!</p> <p>What\'s the point of going out? We\'re just going to wind up back here anyway. I\'m normally not a praying man, but if you\'re up there, please save me, Superman. Your guilty consciences may make you vote Democratic, but secretly you all yearn for a Republican president to lower taxes, brutalize criminals, and rule you like a king!</p>',
					    '<p>Brace yourselves gentlemen. According to the gas chromatograph, the secret ingredient is&hellip; Love!? Who\'s been screwing with this thing? Oh, a *sarcasm* detector. Oh, that\'s a *really* useful invention! This is the greatest case of false advertising I\'ve seen since I sued the movie "The Never Ending Story." And now, in the spirit of the season: start shopping. And for every dollar of Krusty merchandise you buy, I will be nice to a sick kid. For legal purposes, sick kids may include hookers with a cold.</p> <p>And now, in the spirit of the season: start shopping. And for every dollar of Krusty merchandise you buy, I will be nice to a sick kid. For legal purposes, sick kids may include hookers with a cold. And now, in the spirit of the season: start shopping. And for every dollar of Krusty merchandise you buy, I will be nice to a sick kid. For legal purposes, sick kids may include hookers with a cold. D\'oh. Inflammable means flammable? What a country. Kids, we need to talk for a moment about Krusty Brand Chew Goo Gum Like Substance. We all knew it contained spider eggs, but the hantavirus? That came out of left field. So if you\'re experiencing numbness and/or comas, send five dollars to antidote, PO box&hellip; Dad didn\'t leave&hellip; When he comes back from the store, he\'s going to wave those pop-tarts right in your face!</p>'
					  ],
		timers:{},
		init:function( jQcell ){
			// This is a Mad Flipper Panel
			var panelType = WarBoard.Panels.MadFlipper;

			// first hide the panel
			WarBoard.flipout( jQcell );

			// set up the panel as a mad flipper panel
			WarBoard.assignPanelClass( jQcell, panelType );

			WarBoard.MadFlipperPanel.toggleFlip( jQcell );
		},
		destroy:function( jQcell ){
			// clear any remaining timers
			for( cellID in WarBoard.MadFlipperPanel.timers )
			{
				clearTimeout( WarBoard.MadFlipperPanel.timers[cellID] );
			}
		},
		toggleFlip:function( jQcell ){
			var cellID = jQcell.get(0).id;
			var flipDelay = 2500;
			if( jQcell.hasClass('flipInY') )
			{
				var rgb=[0,0,0];
				for(var i=0; i<3;i++)
					rgb[i] = Math.floor( Math.random()*255 );

				var js = "jQuery('#"+ cellID +"').html('').css({'background-color':'rgba("+rgb.join(',')+",1)'});";
				WarBoard.flipout( jQcell );
				setTimeout( js, flipDelay-100 );
			}
			else
			{
				var text = WarBoard.MadFlipperPanel.randomPhrases[Math.floor( Math.random()*WarBoard.MadFlipperPanel.randomPhrases.length )];
				jQcell.html( text );
				WarBoard.flipin( jQcell );
				flipDelay = (Math.random()*2000)+5000;
			}
			var timeout = setTimeout( "WarBoard.MadFlipperPanel.toggleFlip( jQuery('#"+ cellID +"') );",
						              flipDelay );
			WarBoard.MadFlipperPanel.timers[cellID] = timeout;
		}
	}
}