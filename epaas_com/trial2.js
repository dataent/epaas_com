setup_signup = function(page) {
	// button for signup event
	if (!page) {
		// fallback
		var page = $('#page-signup,#page-signup-1');
	}

	let domain_input_flag = 0;


	page.find('input[name="site_name"]').on('input', function() {
		domain_input_flag = 1;
		var $this = $(this);
		clearTimeout($this.data('timeout'));
		$this.data('timeout', setTimeout(function() {
			let site_name = $this.val();
			set_availability_status('empty');
			if(site_name.length === 0) {
				return;
			}

			page.find('.availability-status').addClass('hidden');
			var [is_valid, validation_msg] = is_a_valid_site_name(site_name);
			if(is_valid) {
				// show spinner
				page.find('.availability-spinner').removeClass('hidden');
				check_if_available(site_name, function(status) {
					set_availability_status(status, site_name);
					// hide spinner
					page.find('.availability-spinner').addClass('hidden');
				});
			} else {
				set_availability_status('invalid', site_name, validation_msg);
			}
		}, 500));
	});

	function set_availability_status(is_available, site_name, validation_msg) {
		// reset
		page.find('.availability-status').addClass('hidden');
		page.find('.signup-site_name').removeClass('invalid');

		if(typeof is_available === 'string') {
			if(is_available === 'empty') {
				// blank state
			} else if(is_available === 'invalid') {
				// custom validation message
				const form_control = page.find('.signup-site_name').addClass('invalid');
				form_control.find('.validation-message').html(validation_msg || '');
			}
			return;
		}

		page.find('.availability-status').removeClass('hidden');
		if(is_available) {
			// available state
			page.find('.availability-status i').removeClass('octicon-x text-danger');
			page.find('.availability-status i').addClass('octicon-check text-success');

			page.find('.availability-status').removeClass('text-danger');
			page.find('.availability-status').addClass('text-success');
			page.find('.availability-status span').html(`${site_name}.dataenterprise.co is available!`);
		} else {
			// not available state
			page.find('.availability-status i').removeClass('octicon-check text-success');
			page.find('.availability-status i').addClass('octicon-x text-danger');

			page.find('.availability-status').removeClass('text-success');
			page.find('.availability-status').addClass('text-danger');
			page.find('.availability-status span').html(`${site_name}.dataenterprise.co is already taken.`);
		}
	}

	page.find('.btn-request').off('click').on('click', function() {
		var args = Array.from(page.find('form input'))
			.reduce(
				(acc, input) => {
					acc[$(input).attr('name')] = $(input).val();
					return acc;
				}, {});
		args.site_name = args.site_name.toLowerCase();

		// all mandatory
		if(!( args.site_name)) {
			dataent.msgprint("All fields are necessary. Please try again.");
			return false;
		}

		// validate inputs
		const validations = Array.from(page.find('.form-group.invalid'))
			.map(form_group => $(form_group).find('.validation-message').html());
		// console.log(validations)
		if(validations.length > 0) {
			dataent.msgprint(validations.join("<br>"));
			return;
		}

		// add plan to args
		var plan = get_url_arg('plan');
		if(plan) args.plan = plan;

		var res = get_url_arg('res');
		if(res) args.res = res;

		args.distribution = window.epaas_signup.distribution;

		var $btn = $('.btn-request');

		var btn_html = $btn.html();
		$btn.prop("disabled", true).html("Sending details...");

		goog_report_conversion(); // eslint-disable-line

		console.log("BEFORE SENDING");

		// on success, it will show message page!
		dataent.call({
			method: '.bench_manager.doctype.site.create_site',
			args: args,
			type: 'POST',
			btn: $btn,
			callback: function(r) {
				if (r.exc) return;

				if (r.message.location) {
					window.location.href = r.message.location;
				}
			},

		}).always(function() {
			$btn.prop("disabled", false).html(btn_html);
		});

		return false;
	});


	// change help description based on site_name change
	$('[name="site_name"]').on("keyup", function() {
		$('.site_name-help').text($(this).val() || window.epaas_signup.site_name_placeholder);
	});

	// distribution
	// $('.epaas-distribution').on("click", function() {
	// 	set_distribution(true);
	// });
	//
	// set_distribution();

	function is_a_valid_site_name(site_name) {
		var MIN_LENGTH = 4;
		var MAX_LENGTH = 20;
		if(site_name.length < MIN_LENGTH) {
			return [0, `Sub-domain cannot have less than ${MIN_LENGTH} characters`];
		}
		if(site_name.length > MAX_LENGTH) {
			return [0, `Sub-domain cannot have more than ${MAX_LENGTH} characters`];
		}
		if(site_name.search(/^[A-Za-z0-9][-A-Z-a-z0-9]*[A-Za-z0-9]$/)===-1) {
			return [0, 'Sub-domain can only contain letters and numbers'];
		}
		return [1, ''];
	}

	

	var query_params = dataent.utils.get_query_params();
	if (!query_params.plan) {
		// redirect to pricing page
		var url = window.epaas_signup.distribution=='schools' ? "/schools/pricing" : '/pricing';
		window.location.href = url + '?' + $.param( query_params )

	} else if (query_params.for_mobile_app) {
		// for mobile app singup, hide header and footer
		$("header,footer").addClass("hidden");
	}

	page.find(".plan-message").text("Free 30-day Trial");

	// if (['Free', 'Free-Solo'].indexOf(query_params.plan)!==-1) {
// 		// keeping Free-Solo for backward compatibility
// 		page.find(".plan-message").text("Free for 1 User");
// 	}

	$('.domain-missing-msg').addClass("hidden");
	if (query_params.domain) {
		var site_name = query_params.domain;
		if (site_name.indexOf(".dataenterprise.co")) {
			site_name = site_name.replace(".dataenterprise.co", "");
		}
		$('[name="site_name"]').val(site_name);

		$('.missing-domain').html(query_params.domain);
		$('.missing-domain-msg').removeClass("hidden");
	}

};




dataent.ready(function() {
		setup_signup($('#page-signup'));
	});

