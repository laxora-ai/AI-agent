resource "aws_cloudwatch_event_bus" "poc" {
  name = "${local.name_prefix}-bus-${local.name_suffix}"

  tags = local.tags
}

resource "aws_cloudwatch_event_rule" "appointment_cancelled" {
  name           = "${local.name_prefix}-appointment-cancelled-${local.name_suffix}"
  description    = "Triggers waitlist reactor when an appointment is cancelled."
  event_bus_name = aws_cloudwatch_event_bus.poc.name

  event_pattern = jsonencode({
    source      = ["laxora.agent"]
    detail-type = ["appointment.cancelled"]
  })

  tags = local.tags
}

resource "aws_cloudwatch_event_target" "waitlist_reactor" {
  rule           = aws_cloudwatch_event_rule.appointment_cancelled.name
  event_bus_name = aws_cloudwatch_event_bus.poc.name
  target_id      = "waitlist-reactor"
  arn            = aws_lambda_function.waitlist_reactor.arn
}

resource "aws_lambda_permission" "allow_eventbridge_waitlist" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.waitlist_reactor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.appointment_cancelled.arn
}
