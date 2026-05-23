part of 'write_sample_cubit.dart';

sealed class WriteSampleState {}

final class WriteSampleInitial extends WriteSampleState {}

final class Writing extends WriteSampleState {}

class WriteSampleSuccess extends WriteSampleState {
  final SampleEntity item;
  WriteSampleSuccess(this.item);
}

final class ItemCreated extends WriteSampleSuccess {
  ItemCreated(super.item);
}

final class ItemUpdated extends WriteSampleSuccess {
  ItemUpdated(super.item);
}

final class ItemDeleted extends WriteSampleSuccess {
  ItemDeleted(super.item);
}

final class WriteSampleError extends WriteSampleState {
  final String message;
  WriteSampleError(this.message);
}